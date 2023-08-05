#include "mesh.h"

#include <cstdint>
#include <set>

#include "akida/np.h"
#include "infra/hardware_driver.h"
#include "infra/registers_common.h"
#include "np.h"
#include "registers_top_level.h"

namespace akida {

namespace mesh {

struct MeshInfo {
  uint8_t row_count;
  uint8_t col_count;
  uint8_t nps_per_node;
  uint8_t dma_node_empty;
  uint8_t dma_row;
  uint8_t dma_col;
  uint8_t dma_event_id;
  uint8_t dma_conf_id;
  uint8_t row1_start_col;
  uint8_t row2_start_col;
  uint8_t fnp2_row;
  uint8_t fnp2_col;
  uint8_t last_row_col_count;
};

static bool should_add_np(const np::Ident& np, const MeshInfo& info) {
  // cannot scan DMAs, but other NPs in the DMA node can be scanned, if any.
  // note that row and column in dma_event_ and dma_config are the same
  if (np.row == info.dma_row && np.col == info.dma_col) {
    if (info.dma_node_empty || np.id == info.dma_event_id ||
        np.id == info.dma_conf_id) {
      return false;
    } else {
      return true;
    }
  }
  // Nps in the FNP2 node should be scanned
  if (np.row == info.fnp2_row && np.col == info.fnp2_col) {
    return true;
  }
  // Columns and rows indexes actually start at 1, but for some reason the value
  // 0 can be found in the HW registers, meaning we don't have to skip any
  // column, so it is equivalent to starting at column 1
  uint8_t start_col_r1 = info.row1_start_col == 0 ? 1 : info.row1_start_col;
  uint8_t start_col_r2 = info.row2_start_col == 0 ? 1 : info.row2_start_col;
  // skip empty nodes
  if ((np.row == 1 && np.col < start_col_r1) ||
      (np.row == 2 && np.col < start_col_r2) ||
      (np.row == info.row_count && np.col > info.last_row_col_count)) {
    return false;
  }
  return true;
}

void add_nps(const MeshInfo& info, HardwareDeviceImpl* device,
             std::vector<np::Info>* nps) {
  // scan mesh to know types for each NP
  for (uint8_t col = 1; col <= info.col_count; ++col) {
    for (uint8_t row = 1; row <= info.row_count; ++row) {
      // increase priority if node has FNP3
      for (uint8_t id = 0; id < info.nps_per_node; ++id) {
        np::Ident np{col, row, id};
        // Check if np scan should be skipped
        if (!should_add_np(np, info))
          continue;
        auto types = np::get_types(device, np);
        if (types.empty()) {
          panic("Error detecting NP type.");
        }

        // store np
        nps->emplace_back(np::Info({np, types}));
      }
    }
  }
}

static MeshInfo read_mesh_info(const HardwareDriver& driver,
                               const HwVersion& version) {
  const auto top_level_reg_offset = driver.top_level_reg();
  // Read mesh info registers
  auto reg = driver.read32(top_level_reg_offset + REG_MESH_INFO1);
  MeshInfo info;
  info.row_count = static_cast<uint8_t>(get_field(reg, MESH_ROWS));
  info.col_count = static_cast<uint8_t>(get_field(reg, MESH_COLS));
  info.row1_start_col = static_cast<uint8_t>(get_field(reg, R1_START_COL));
  info.row2_start_col = static_cast<uint8_t>(get_field(reg, R2_START_COL));
  // Note that hardware can report 0xff or a value > than row count if no
  // "common" node. A common node does not contain FNP2 or DMA. In this case the
  // row will not be scanned, unless it contains a FNP2 node.
  reg = driver.read32(top_level_reg_offset + REG_MESH_INFO2);
  info.nps_per_node = static_cast<uint8_t>(get_field(reg, NP_PER_NODE));
  info.dma_node_empty = static_cast<uint8_t>(get_field(reg, DMA_NODE_EMPTY));
  info.dma_row = static_cast<uint8_t>(get_field(reg, DMA_NODE_ROW));
  info.dma_col = static_cast<uint8_t>(get_field(reg, DMA_NODE_COL));
  info.dma_event_id = static_cast<uint8_t>(get_field(reg, DMA_AE_NP));
  info.dma_conf_id = static_cast<uint8_t>(get_field(reg, DMA_CFG_NP));

  reg = driver.read32(top_level_reg_offset + REG_MESH_INFO3);
  info.fnp2_col = static_cast<uint8_t>(get_field(reg, FNP2_COL));
  info.fnp2_row = static_cast<uint8_t>(get_field(reg, FNP2_ROW));
  // On NSoC_v2, field COL_NUM_LAST_NP does not exist, so it is initialized to
  // MESH_COLS for compatibility (assuming last row has same column count as
  // other rows)
  if (version == NSoC_v2) {
    info.last_row_col_count = info.col_count;
  } else {
    info.last_row_col_count =
        static_cast<uint8_t>(get_field(reg, COL_NUM_LAST_NP));
  }
  return info;
}

std::unique_ptr<np::Mesh> discover(HardwareDeviceImpl* device) {
  auto device_mesh = std::unique_ptr<np::Mesh>(new np::Mesh());
  auto info = read_mesh_info(*device->driver(), device->version());
  // Store DMA endpoints locations
  device_mesh->dma_event =
      np::Ident{info.dma_col, info.dma_row, info.dma_event_id};
  device_mesh->dma_conf =
      np::Ident{info.dma_col, info.dma_row, info.dma_conf_id};
  // Now build NPs descriptions used to assign NPs in the Mesh
  add_nps(info, device, &device_mesh->nps);
  return device_mesh;
}

}  // namespace mesh

}  // namespace akida
