#pragma once

#define ROTR64(x, y) (((x) >> (y)) | ((x) << ((64 - (y)) & 63)))
#define ROTL64(x, y) (((x) << (y)) | ((x) >> ((64 - (y)) & 63)))
#define ROTR32(x, y) (((x) >> (y)) | ((x) << ((32 - (y)) & 31)))
#define ROTL32(x, y) (((x) << (y)) | ((x) >> ((32 - (y)) & 31)))

#include <stdint.h>

// Specific integer types:
#define uint64_cu unsigned long long int
#define uint32_cu unsigned int

static_assert(sizeof(uint64_cu) == sizeof(uint64_t),
    "uint64_cu must be an unsigned 64-bit integer");

static_assert(sizeof(uint32_cu) == sizeof(uint32_t),
    "uint32_cu must be an unsigned 32-bit integer");

#define _DI_ __attribute__((always_inline)) __device__ inline

#if CUDART_VERSION >= 9000
#define shuffle_32(x, y) __shfl_sync(0xffffffffu, (x), (y))
#define shuffle_xor_32(x, y) __shfl_xor_sync(0xffffffffu, (x), (y))
#define ballot_32(p) __ballot_sync(0xffffffffu, (p))
#else
#define shuffle_32(x, y) __shfl((x), (y))
#define shuffle_xor_32(x, y) __shfl_xor((x), (y))
#define ballot_32(p) __ballot(p)
#endif

