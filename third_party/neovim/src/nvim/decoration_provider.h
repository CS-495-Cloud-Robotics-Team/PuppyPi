#pragma once

#include <stdbool.h>
#include <stdint.h>

#include "klib/kvec.h"
#include "nvim/buffer_defs.h"  // IWYU pragma: keep
#include "nvim/macros_defs.h"
#include "nvim/types_defs.h"

#define DP_MAX_ERROR 3

typedef struct {
  NS ns_id;
  bool active;
  LuaRef redraw_start;
  LuaRef redraw_buf;
  LuaRef redraw_win;
  LuaRef redraw_line;
  LuaRef redraw_end;
  LuaRef hl_def;
  LuaRef spell_nav;
  int hl_valid;
  bool hl_cached;

  uint8_t error_count;
} DecorProvider;

typedef kvec_withinit_t(DecorProvider *, 4) DecorProviders;

EXTERN bool provider_active INIT( = false);

#ifdef INCLUDE_GENERATED_DECLARATIONS
# include "decoration_provider.h.generated.h"
#endif
