#pragma once

#include <stdint.h>
#include <stdlib.h>
#include <vector>
#include <cstring>
#include <iostream>

namespace apg {

/**
 * Zero-allocate a block of memory aligned on a cache line.
 */
void* zalloc(uint64_t numbytes) {

    #ifdef __CYGWIN__
        return calloc(1, numbytes);
    #else
        #ifdef _WIN32
            return calloc(1, numbytes);
        #else
            void* nextarray;
            if (posix_memalign(&nextarray, 64, numbytes)) {
                std::cerr << "Memory error!!!" << std::endl;
                return 0;
            }
            std::memset(nextarray, 0, numbytes);
            return nextarray;
        #endif
    #endif

}

template <typename K, typename I, typename V>
struct kiventry {

    K key;
    I next;
    I gcflags; // For gc and ensuring nice standard layout.
    V value;

};

/**
 * Function for reducing a 64-bit hash into a log2(modulus)-bit hash,
 * where modulus is a power of two.
 */
struct DyadicHashReducer {

    int shiftamt;

    void resize(uint64_t modulus) {

        // This operation _might_ be slow (e.g. if there is no
        // hardware support for CTZ), so we perform this once
        // when we first create or later resize the table.
        shiftamt = 64 - __builtin_ctzll(modulus);

    }

    explicit DyadicHashReducer(uint64_t modulus) {

        // Compute the shift amount:
        resize(modulus);

    }

    uint64_t nextsize() const {

        return 1ull << (65 - shiftamt);

    }

    uint64_t reduce(uint64_t full_hash) const {

        // We use the output function of Melissa O'Neill's PCG PRNG,
        // since it's a uniform way to collapse a 64-bit integer into
        // a smaller range. Also, the good mixing qualities of the
        // output function should compensate for a weak hash function.

        // Apply a permutation sigma : uint64_t --> uint64_t
        uint64_t xorshifted = ((full_hash >> ((full_hash >> 59u) + 5u)) ^ full_hash);

        // Fibonacci hashing:
        // https://probablydance.com/2018/06/16/fibonacci-hashing-the-optimization-that-the-world-forgot-or-a-better-alternative-to-integer-modulo/
        xorshifted *= 11400714819323198485ull;

        // Collapse to the desired range:
        return (xorshifted >> shiftamt);

    }

};

template <typename K, typename I, typename V, typename HashReducer = DyadicHashReducer>
class strashtable {

    public:

    const static int klowbits = 9;
    I gccounter;

    private:

    // std::vector<kiventry<K, I, V>> nodes;
    std::vector<kiventry<K, I, V>*> arraylist;

    I totalnodes;
    I freenodes;

    std::vector<I> hashtable;

    HashReducer hr;

    // Get the next free node:
    I getfreenode() {
        if (freenodes == 0) {

            freenodes = arraylist.size() << klowbits;

            auto nextarray = (kiventry<K, I, V>*) zalloc(sizeof(kiventry<K, I, V>) << klowbits);

            arraylist.push_back(nextarray);

            for (int i = 0; i < ((1 << klowbits) - 1); i++) {
                nextarray[i].next = freenodes + i + 1;
                nextarray[i].gcflags = 0;
            }

        }
        return freenodes;
    }

    // New node with specified value:
    I newnode(const K &key, const I &next, const V &value) {
        I r = getfreenode();
        kiventry<K, I, V>* fptr = ind2ptr(r);
        freenodes = fptr->next;
        fptr->key = key;
        fptr->next = next;
        fptr->value = value;
        totalnodes += 1;
        return r;
    }

    void create_null_element() {

        freenodes = 0;
        totalnodes = 0;
        gccounter = 0;

        discard_node();

    }

    public:

    I discard_node() {

        I r = getfreenode();
        kiventry<K, I, V>* fptr = ind2ptr(r);
        freenodes = fptr->next;
        fptr->next = 0;
        totalnodes += 1;
        return r;

    }

    explicit strashtable(uint64_t hashsize) : hashtable(hashsize, 0), hr(hashsize) {

        create_null_element();

    }

    void teardown() {
        while (!arraylist.empty()) {
            free(arraylist.back());
            arraylist.pop_back();
        }
    }

    void clear() {
        teardown();
        for (uint64_t i = 0; i < hashtable.size(); i++) {
            hashtable[i] = 0;
        }
        create_null_element();
    }

    ~strashtable() {
        teardown();
    }

    // Convert index to pointer:
    kiventry<K, I, V>* ind2ptr(I index) {
        // return (&(nodes[index]));
        return &(arraylist[index >> klowbits][index & ((1 << klowbits) - 1)]);
    }

    kiventry<K, I, V>& operator[](I index) {
        return *ind2ptr(index);
    }

    uint64_t size() const {
        return totalnodes;
    }

    uint64_t hashsize() const {
        return hashtable.size();
    }

    uint64_t max_size() const {
        return arraylist.max_size();
    }

    /**
     * We use hash chaining, so the container will continue to work even
     * when the load ratio `((double) nodes.size()) / hashtable.size()`
     * grows larger than 1. However, large load ratios will result in
     * lots of pointer indirection before finding the desired element,
     * so we should grow the hashtable to maintain a low load ratio.
     */
    void resize_hash(uint64_t newsize) {

        if (newsize == hashtable.size()) {
            // nothing to do here:
            return;
        }

        // Create a new hashtable:
        std::vector<I> newtable(newsize, 0);
        hr.resize(newsize);

        // Based on code by Tom Rokicki:
        for (uint64_t i = 0; i < hashtable.size(); i++) {
            I p = hashtable[i];
            while (p) {
                kiventry<K, I, V>* pptr = ind2ptr(p);
                I np = pptr->next;
                uint64_t h = hr.reduce(pptr->key.hash());
                pptr->next = newtable[h];
                newtable[h] = p;
                p = np; // contrary to the beliefs of most complexity theorists.
            }
        }

        hashtable.swap(newtable);

    }

    void resize_if_necessary() {
        if (totalnodes > hashtable.size()) {
            resize_hash(hr.nextsize());
        }
    }

    template<typename T, typename FnMatch, typename FnDefault>
    T lookupkey(const K &key, const T &null_value, FnMatch lambda_match, FnDefault lambda_default) {

        if (key.iszero()) { return null_value; }
        uint64_t h = hr.reduce(key.hash());

        // iterate over hash bucket:
        I p = hashtable[h];
        kiventry<K, I, V>* predptr = nullptr;
        while (p) {
            kiventry<K, I, V>* pptr = ind2ptr(p);
            if (pptr->key == key) {
                return lambda_match(p, h, predptr, pptr);
            }
            predptr = pptr;
            p = pptr->next;
        }

        // not in the hashtable
        return lambda_default(h);
    }

    template<bool makenew, bool overwrite>
    I touchnode(const K &key, const V &value) {

        return lookupkey(key, (I) 0,

            [&](I p, uint64_t h, kiventry<K, I, V>* predptr, kiventry<K, I, V>* pptr) {
                // Set the value:
                if (overwrite) { pptr->value = value; }
                if (predptr) {
                    // Move this node to the front:
                    predptr->next = pptr->next;
                    pptr->next = hashtable[h];
                    hashtable[h] = p;
                }
                return p;
            },

            [&](uint64_t h) {
                if (makenew) {
                    I p = newnode(key, hashtable[h], value);
                    hashtable[h] = p;
                    resize_if_necessary();
                    return p;
                } else {
                    return ((I) -1);
                }
            }
        );
    }

    template<typename Fn>
    bool fancy_erase(const K &key, Fn lambda) {

        return lookupkey(key, false,

            [&](I p, uint64_t h, kiventry<K, I, V>* predptr, kiventry<K, I, V>* pptr) {

                // Remove from hashtable:
                if (predptr) {
                    predptr->next = pptr->next;
                } else {
                    hashtable[h] = pptr->next;
                }

                lambda(p, pptr);
                return true;
            },

            [&](uint64_t h) {
                (void) h;
                return false;
            }
        );
    }

    bool erasenode(const K &key) {

        return fancy_erase(key, [&](I p, kiventry<K, I, V>* pptr) {
            // Reset memory:
            std::memset(pptr, 0, sizeof(kiventry<K, I, V>));

            // Prepend to list of free nodes:
            pptr->next = freenodes;
            freenodes = p;

            // We've reduced the total number of nodes:
            totalnodes -= 1;
        });
    }

    void changekey(const K &oldkey, const K &newkey) {

        if (newkey.iszero()) {
            erasenode(oldkey);
            return;
        }

        fancy_erase(oldkey, [&](I p, kiventry<K, I, V>* pptr) {
            // Change key in situ:
            pptr->key = newkey;

            // Reintroduce into hashtable:
            uint64_t h2 = hr.reduce(newkey.hash());
            pptr->next = hashtable[h2];
            hashtable[h2] = p;
        });
    }

    template<bool DeleteUnmarked>
    void gc_traverse() {
        for (uint64_t i = 0; i < hashtable.size(); i++) {
            I p = hashtable[i];
            kiventry<K, I, V>* predptr = nullptr;
            while (p) {
                kiventry<K, I, V>* pptr = ind2ptr(p);
                I np = pptr->next;
                if (DeleteUnmarked && (pptr->gcflags == 0)) {
                    // Remove from hashtable:
                    if (predptr) {
                        predptr->next = np;
                    } else {
                        hashtable[i] = np;
                    }

                    // Reset memory:
                    std::memset(pptr, 0, sizeof(kiventry<K, I, V>));

                    // Prepend to list of free nodes:
                    pptr->next = freenodes;
                    freenodes = p;

                    // We've reduced the total number of nodes:
                    totalnodes -= 1;
                } else {

                    // Node still exists; zero the flags:
                    pptr->gcflags = 0;
                    predptr = pptr;
                }
                // Contrary to the belief of most complexity theorists:
                p = np;
            }
        }

        gccounter = 0;
    }


};

}

