#pragma once

#include <cstdint>
#include "infra/registers_common.h"

namespace akida {

static constexpr uint32_t EPG_REG_BASE = 0x00040000;
static inline uint32_t epg_reg_base(const uint32_t top_level_reg_base) {
  return top_level_reg_base + EPG_REG_BASE;
}

// AE Control Register
static constexpr uint32_t AE_CTRL_REG = 0x0;
static constexpr RegDetail AE_IB_MODE(0, 3);
static constexpr RegDetail EVENT_SIZE(8, 11);
static constexpr RegDetail IJ_IB_SWAP(12);
static constexpr RegDetail IJ_OB_SWAP(13);
static constexpr RegDetail LOOPBACK_MODE(16);
static constexpr RegDetail PKT_COUNT_EN(17);
static constexpr RegDetail SOFT_RESET(20);
static constexpr RegDetail SEQ_ID_RESET(24);

// NoC Burst Delay register
static constexpr uint32_t NOC_BURST_DELAY_REG = 0x4;
static constexpr RegDetail NOC_BURST_DELAY(0, 15);

// Inter Packet delay register
static constexpr uint32_t INTER_PACKET_DELAY_REG = 0x8;
static constexpr RegDetail PKT_DELAY(0, 15);

// Sync packet delay register
static constexpr uint32_t SYNC_PACKET_DELAY_REG = 0xC;
static constexpr RegDetail SYNC_PACKET_DELAY(0, 15);
static constexpr RegDetail IB_SYNC_PACKET_DELAY(16, 26);

// Header Packet Description register
static constexpr uint32_t HDR_PACKET_DESC_REG = 0x10;
static constexpr RegDetail HDR_PKT_TYPE(0, 3);
static constexpr RegDetail DEST_NP(4, 7);
static constexpr RegDetail DEST_ROW(16, 23);
static constexpr RegDetail DEST_COL(24, 31);
static constexpr RegDetail DEST_WEST_COL = DEST_ROW;
static constexpr RegDetail DEST_EAST_COL = DEST_COL;

// Payload Packet Description register
static constexpr uint32_t PAYLOAD_PACKET_DESC_REG = 0x14;
static constexpr RegDetail DEST_LAYER(8, 15);

// Sync packet control register
static constexpr uint32_t SYNC_PACKET_DESC_REG = 0x18;
static constexpr RegDetail TOTAL_SRC_NP(0, 7);
static constexpr RegDetail SRC_LAYER(8, 15);
static constexpr RegDetail LAST_LAYER(16, 23);
static constexpr RegDetail END_LAYER(24, 31);

// Event packet control register
static constexpr uint32_t EVENT_PACKET_CTRL_REG = 0x1C;
static constexpr RegDetail PACKET_SIZE(0, 22);
static constexpr RegDetail BUF_MODE(24);
static constexpr RegDetail FLUSH_EN(25);
static constexpr uint32_t EPG_MAX_PACKET_SIZE = 0x7fffff;

// Event buffer control register
static constexpr uint32_t EVENT_BUFFER_CTRL_REG = 0x20;
static constexpr RegDetail EVENT_BUF_MAX(0, 30);

// Sync Packet Last Layer register
static constexpr uint32_t SYNC_PKT_LAST_LAYER_REG = 0x24;
static constexpr RegDetail EOP_SRC_LAYER_EN(0);
static constexpr RegDetail MM_DEST_LAYER_EN(4);
static constexpr RegDetail EOP_SRC_LAYER(8, 22);

// Inbound packet buffer event counter - debug only register
static constexpr uint32_t IB_PACKET_BUFFER_CNT_REG = 0x40;
static constexpr RegDetail IB_EVENT_COUNT(0, 30);

// Outbound packet buffer event counter - debug only register
static constexpr uint32_t OB_PACKET_BUFFER_CNT_REG = 0x44;
static constexpr RegDetail OB_EVENT_RECEIVED_COUNT(0, 15);
static constexpr RegDetail OB_EVENT_ACCEPTED_COUNT(16, 31);

// Don't consider debug regs
constexpr auto EPG_REGISTERS_LENGTH = EVENT_BUFFER_CTRL_REG + 1;

// Useful for formatting
enum class PacketType {
  Broadcast = 0x0,
  LimitedBroadcast = 0x1,
  Point2Point = 0x2,
};

}  // namespace akida
