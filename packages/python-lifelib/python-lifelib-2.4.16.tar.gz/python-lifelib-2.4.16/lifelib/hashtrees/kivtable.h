/*
* (key, index, value) hashtables that can be addressed by either the
* key (like a regular associative array) or the (typically 32-bit)
* index integer.
*/

#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <vector>
#include <cstring>
#include "numtheory.h"
#include <iostream>
#include <unordered_map>

#include "strashtable.hpp"


namespace apg {

    const static uint32_t klowbits = 8;

    template <typename T, typename I, int B>
    class metaarray {

        std::vector<T*> arraylist;

        public:

        I totalnodes = 0;

        T* ind2ptr(I index) {
            return (arraylist[index >> B] + (index & ((1 << B) - 1)));
        }

        T* newnode() {
            if ((totalnodes & ((1 << B) - 1)) == 0) {
                T* nextarray = (T*) zalloc(sizeof(T) << B);
                arraylist.push_back(nextarray);
            }
            return ind2ptr(totalnodes++);
        }

        explicit metaarray() = default;

        ~metaarray() {

            while (!arraylist.empty()) {
                free(arraylist.back());
                arraylist.pop_back();
            }

        }

    };

    template <typename K, typename V, typename I=uint32_t>
    class indirected_map {
        /*
        * Similar to an unordered_map, but the values are contiguous in
        * memory instead of being adjacent to their keys.
        */

        public:

        metaarray<V, I, 5> elements;
        std::unordered_map<K, V*> hashtable;

        V& operator[](K key) {

            V** pointer_to_pointer = &(hashtable[key]);
            if (*pointer_to_pointer == 0) {
                *pointer_to_pointer = elements.newnode();
            }
            return **pointer_to_pointer;

        }


    };

    template <typename K, typename I, typename V>
    class kivtable : public strashtable<K, I, V> {

        public:

        uint64_t total_bytes() const {
            uint64_t nodemem = sizeof(kiventry<K, I, V>) * this->size();
            uint64_t hashmem = sizeof(I) * this->hashsize();
            return (nodemem + hashmem);
        }

        // Get node index from key:
        I getnode(const K &key, bool makenew) {

            V blank;
            memset(&blank, 0, sizeof(blank));

            if (makenew) {
                return this->template touchnode<true, false>(key, blank);
            } else {
                return this->template touchnode<false, false>(key, blank);
            }
        }

        // Create a (key, value) pair and return index:
        I setnode(const K &key, const V &value) {

            return this->template touchnode<true, true>(key, value);

        }

        explicit kivtable() : strashtable<K, I, V>(4096) { }

    };

    /*
    template <typename K, typename V>
    using kivtable32 = kivtable<K, uint32_t, V>;

    template <typename K, typename V>
    using kivtable64 = kivtable<K, uint64_t, V>;
    */

}

