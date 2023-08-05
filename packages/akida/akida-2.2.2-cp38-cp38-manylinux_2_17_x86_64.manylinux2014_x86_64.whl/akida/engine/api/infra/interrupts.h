#pragma once

#if defined(__cplusplus)
extern "C" { /* C-declarations in C++ programs */
#endif

/**
 * @brief List of the possible interrupt request sources.
 */
enum akida_interrupt {
  DMA_HRC_IRQ,
  DMA_CONFIG_IRQ,
  DMA_EVENTS,
};

#if defined(__cplusplus)
} /* C-declarations in C++ programs */
#endif