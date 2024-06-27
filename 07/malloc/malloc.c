//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_BINS 8 // binの数

// int debug_cnt = 0;
//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//

my_heap_t bins[NUM_BINS]; // 32,64,128,256,512,1024,2048,4096
static my_metadata_t dummy = {0, NULL}; // Use static to prevent duplicate initialization of dummy
size_t bin_sizes[NUM_BINS] = {32, 64, 128, 256, 512, 1024, 2048, 4096};

//
// Helper functions (feel free to add/remove/edit!)
//

// Determine which bin size is appropriate
size_t get_bin_index(size_t size) {
    for (int i = 0; i < NUM_BINS; i++) {
        if (size <= bin_sizes[i]) return i;
    }
    return -1;
}

// Add a free region to the bin
void my_add_to_free_list(my_metadata_t *metadata) {
  size_t bin_index = get_bin_index(metadata->size);
  assert(bin_index >= 0);
  assert(!metadata->next);
  metadata->next = bins[bin_index].free_head;
  bins[bin_index].free_head = metadata;
}

// Remove the desired region from the bin
void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  assert(metadata);
  size_t bin_index = get_bin_index(metadata->size);
  assert(bin_index >= 0);
  if (prev) {
    prev->next = metadata->next;
  } else {
    bins[bin_index].free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < NUM_BINS; i++) {
    bins[i].free_head = &dummy;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  size_t bin_index = get_bin_index(size);
  assert(bin_index >= 0);
  my_metadata_t *metadata = NULL;
  my_metadata_t *prev = NULL;
  my_metadata_t *bestfit = NULL;
  my_metadata_t *bestfit_prev = NULL;

  // Best-fit: Find the smallest free slot that fits the object.
  for(int i = bin_index; i < NUM_BINS; i++){

    metadata = bins[i].free_head;

    while (metadata) {
        if (metadata->size >= size && (!bestfit || metadata->size < bestfit->size)){
            bestfit_prev = prev;
            bestfit = metadata;
        }
        prev = metadata;
        metadata = metadata->next;
    }
    if(metadata){
        break;
    }
    metadata = bestfit;
    prev = bestfit_prev;

  }

  if (!metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;

    // Add the memory region to the free list.
    my_add_to_free_list(metadata);

    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
