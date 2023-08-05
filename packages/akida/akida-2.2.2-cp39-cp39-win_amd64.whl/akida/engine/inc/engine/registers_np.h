#pragma once

#include <cstdint>
#include "infra/registers_common.h"

namespace akida {

// REGISTER 1
static constexpr uint32_t REGISTER_1 = 0x00 / 4;
static constexpr RegDetail REG1_VERSION(0, 3);
static constexpr RegDetail REG1_FNP_INSTAL(4, 5);
static constexpr RegDetail REG1_CNP_INSTAL(6, 7);
static constexpr RegDetail REG1_NP_INDEX(12, 15);
static constexpr RegDetail REG1_NP_COL(16, 23);
static constexpr RegDetail REG1_NP_ROW(24, 31);

// REGISTER 2
static constexpr uint32_t REGISTER_2 = 0x04 / 4;
static constexpr RegDetail REG2_FNP_MODE(4);
static constexpr RegDetail REG2_STOP_CLK_EN(5);
static constexpr RegDetail REG2_SRAM_LP_EN(6);
static constexpr RegDetail REG2_SRAM_CNP2FNP_EN(7);
static constexpr RegDetail REG2_NP_LAYER_ID(8, 15);
static constexpr RegDetail REG2_FNP2_ID(16, 19);
static constexpr RegDetail REG2_NP2NP_CFG(20, 21);
static constexpr RegDetail REG2_PKSRAM_1B_MODE(22);
static constexpr RegDetail REG2_PKSRAM_4FILTER(23);
static constexpr RegDetail REG2_CNP4FNP_NUM(24, 25);

// REGISTER 3
static constexpr uint32_t REGISTER_3 = 0x08 / 4;
static constexpr RegDetail REG3_ERROR_SEQ(0);
static constexpr RegDetail REG3_ERROR_SEQ_EN(1);
static constexpr RegDetail REG3_ERROR_FC(2);
static constexpr RegDetail REG3_ERROR_FC_EN(3);
static constexpr RegDetail REG3_KEEP_IB_SPIKES(7);
static constexpr RegDetail REG3_INTR_NP_INDEX(12, 15);
static constexpr RegDetail REG3_INTR_NP_COL(16, 23);
static constexpr RegDetail REG3_INTR_NP_ROW(24, 31);

// REGISTER 4
static constexpr uint32_t REGISTER_4 = 0x0c / 4;
static constexpr RegDetail REG4_IB_BWIDTH(0, 1);
static constexpr RegDetail REG4_SEPARABLE(2);
static constexpr RegDetail REG4_LGC_4B_EN(3);
static constexpr RegDetail REG4_DW_BWIDTH(4, 5);
static constexpr RegDetail REG4_FW_BWIDTH(4, 5);
static constexpr RegDetail REG4_FW_NEG_EN(7);
static constexpr RegDetail REG4_PW_BWIDTH(8, 9);
static constexpr RegDetail REG4_OB_BWIDTH(12, 13);
static constexpr RegDetail REG4_OB_QUANTIZE(15);
static constexpr RegDetail REG4_NP_NUM(16, 23);
static constexpr RegDetail REG4_NP_LAYER(24, 31);

// REGISTER 5
static constexpr uint32_t REGISTER_5 = 0x10 / 4;
static constexpr RegDetail REG5_PKSRAM_SIZE(0, 17);
static constexpr RegDetail REG5_INIT_PKSRAM(31);

// REGISTER SRAM LOW POWER
static constexpr uint32_t REGISTER_SRAM_LP = 0x14 / 4;

// REGISTER 6
static constexpr uint32_t REGISTER_6 = 0x18 / 4;
static constexpr RegDetail REG6_IBFIFO_SPACE_LIMIT(16, 20);
static constexpr RegDetail REG6_IBFIFO_USED_LIMIT(24, 28);

// REGISTER 7
static constexpr uint32_t REGISTER_7 = 0x1c / 4;

// REGISTER 8
static constexpr uint32_t REGISTER_8 = 0x20 / 4;
static constexpr RegDetail REG8_II_SIZE(0, 10);
static constexpr RegDetail REG8_II_OFFSET(12, 15);
static constexpr RegDetail REG8_JJ_SIZE(16, 26);
static constexpr RegDetail REG8_JJ_OFFSET(28, 31);

// REGISTER 9
static constexpr uint32_t REGISTER_9 = 0x24 / 4;
static constexpr RegDetail REG9_I_ORIG_CUT(0, 11);
static constexpr RegDetail REG9_I_CONV_STRD_OFFSET(12);
static constexpr RegDetail REG9_J_ORIG_CUT(16, 27);
static constexpr RegDetail REG9_J_CONV_STRD_OFFSET(28);

// REGISTER 10
static constexpr uint32_t REGISTER_10 = 0x28 / 4;
static constexpr RegDetail REG10_I_SIZE_CUT(0, 10);
static constexpr RegDetail REG10_J_SIZE_CUT(16, 26);

// REGISTER 11
static constexpr uint32_t REGISTER_11 = 0x2c / 4;
static constexpr RegDetail REG11_ICONT_SIZE(0, 7);
static constexpr RegDetail REG11_CHCONT_SIZE(12, 21);
static constexpr RegDetail REG11_CH_SIZE(12, 29);

// REGISTER 12
static constexpr uint32_t REGISTER_12 = 0x30 / 4;
static constexpr RegDetail REG12_CNP2FNP_WSRAM_SIZE(24, 31);

// REGISTER 13
static constexpr uint32_t REGISTER_13 = 0x34 / 4;
static constexpr RegDetail REG13_STOP_CLK_DELAY(0, 15);

// REGISTER FNP1
static constexpr uint32_t REGISTER_FNP1 = 0x38 / 4;
static constexpr RegDetail FNP1_FPKT_WSIZE(0, 17);
static constexpr RegDetail FNP1_INIT_PKSRAM(31);

// REGISTER FNP2
static constexpr uint32_t REGISTER_FNP2 = 0x3c / 4;
static constexpr RegDetail FNP2_FN_TOTAL(0, 16);

// REGISTER FNP3
static constexpr uint32_t REGISTER_FNP3 = 0x40 / 4;
static constexpr RegDetail FNP3_OB_N_ORIG(0, 17);
static constexpr RegDetail FNP3_OB_TYPE(28, 29);

// REGISTER FNP4
static constexpr uint32_t REGISTER_FNP4 = 0x44 / 4;
static constexpr RegDetail FNP4_W_SIZE_LAST(0, 15);
static constexpr RegDetail FNP4_W_BLK_COUNT(20, 23);

// REGISTER CNP1
static constexpr uint32_t REGISTER_CNP1 = 0x50 / 4;
static constexpr RegDetail CNP1_PWCONT_SIZE(0, 6);
static constexpr RegDetail CNP1_CONV_STRD(8);
static constexpr RegDetail CNP1_TF1x1_TOTAL(16, 26);
static constexpr RegDetail CNP1_KERNEL_TYPE(28, 30);

// REGISTER CNP2
static constexpr uint32_t REGISTER_CNP2 = 0x54 / 4;
static constexpr RegDetail CNP2_TF_TOTAL(0, 10);
static constexpr RegDetail CNP2_PF_TOTAL(16, 26);

// REGISTER CNP3
static constexpr uint32_t REGISTER_CNP3 = 0x58 / 4;
static constexpr RegDetail CNP3_NF_TOTAL(0, 10);
static constexpr RegDetail CNP3_PW_START_ADDR(16, 29);

// REGISTER CNP4
static constexpr uint32_t REGISTER_CNP4 = 0x60 / 4;
static constexpr RegDetail CNP4_OB_I_ORIG(0, 11);
static constexpr RegDetail CNP4_OB_J_ORIG(16, 27);

// REGISTER CNP5
static constexpr uint32_t REGISTER_CNP5 = 0x64 / 4;
static constexpr RegDetail CNP5_OB_II_SIZE(0, 9);
static constexpr RegDetail CNP5_OB_JJ_SIZE(16, 23);

// REGISTER CNP6
static constexpr uint32_t REGISTER_CNP6 = 0x68 / 4;
static constexpr RegDetail CNP6_OB_CH_ORIG(0, 10);
static constexpr RegDetail CNP6_OB_F_SIZE(16, 26);

// REGISTER CNP7
static constexpr uint32_t REGISTER_CNP7 = 0x6c / 4;
static constexpr RegDetail CNP7_POOL_SIZE(0, 2);
static constexpr RegDetail CNP7_POOL_STRIDE(4, 6);
static constexpr RegDetail CNP7_GLBL_POOLING(8);
static constexpr RegDetail CNP7_PAD_RHT_EN(12);
static constexpr RegDetail CNP7_PAD_LFT_EN(13);
static constexpr RegDetail CNP7_PAD_BOT_EN(14);
static constexpr RegDetail CNP7_PAD_TOP_EN(15);

// REGISTER CNP8
static constexpr uint32_t REGISTER_CNP8 = 0x70 / 4;
static constexpr RegDetail CNP8_CPK_ICONT_SIZE(0, 13);
static constexpr RegDetail CNP8_CPK_CHCONT_SIZE{
    16,
    8,
};

// REGISTER CNP9
static constexpr uint32_t REGISTER_CNP9 = 0x74 / 4;
static constexpr RegDetail CNP9_CPK_CHAIN_EN(0);
static constexpr RegDetail CNP9_CPK_OB_LOOP(16, 23);

// REGISTER PR1
static constexpr uint32_t REGISTER_PR1 = 0x80 / 4;
static constexpr RegDetail PR1_EN(0);
static constexpr RegDetail PR1_FNP_MODE(1);
static constexpr RegDetail PR1_PKSRAM_1B_MODE(2);
static constexpr RegDetail PR1_MERGING_LAYER(3);
static constexpr RegDetail PR1_IB_BWIDTH(4, 5);
static constexpr RegDetail PR1_RCV_NP_LAYER(24, 31);

// REGISTER PR2
static constexpr uint32_t REGISTER_PR2 = 0x84 / 4;
static constexpr RegDetail PR1_I_ORIG_CUT(0, 11);
static constexpr RegDetail PR1_J_ORIG_CUT(16, 27);

// REGISTER PR3
static constexpr uint32_t REGISTER_PR3 = 0x88 / 4;
static constexpr RegDetail PR1_I_SIZE_CUT(0, 10);
static constexpr RegDetail PR1_J_SIZE_CUT(16, 26);

// REGISTER PR4
static constexpr uint32_t REGISTER_PR4 = 0x8c / 4;
static constexpr RegDetail PR1_CPK_ICONT_SIZE(0, 13);
static constexpr RegDetail PR1_CPK_CHCONT_SIZE(16, 24);
static constexpr RegDetail PR1_CH_SIZE(0, 17);

// REGISTER LEARN1
static constexpr uint32_t REGISTER_LEARN1 = 0x90 / 4;
static constexpr RegDetail LEARN1_LTHRESHOLD(0, 19);
static constexpr RegDetail LEARN1_LEARN_MODE(28);

// REGISTER LEARN2
static constexpr uint32_t REGISTER_LEARN2 = 0x94 / 4;
static constexpr RegDetail LEARN2_MIN_NSWAP(0, 15);
static constexpr RegDetail LEARN2_MAX_LOOP(24, 31);

// REGISTER LEARN3
static constexpr uint32_t REGISTER_LEARN3 = 0x98 / 4;
static constexpr RegDetail LEARN3_DELTA_NSWAP(0, 15);
static constexpr RegDetail LEARN3_PKT_CLASS(20, 29);

// REGISTER LEARN4
static constexpr uint32_t REGISTER_LEARN4 = 0x9c / 4;
static constexpr RegDetail LEARN4_IN_CH_COUNT(0, 15);

// REGISTER LEARN5
static constexpr uint32_t REGISTER_LEARN5 = 0xa4 / 4;
static constexpr RegDetail LEARN5_R_FD_ADDR_BASE(0, 11);

// REGISTER MM1
static constexpr uint32_t REGISTER_MM1 = 0xB0 / 4;
static constexpr RegDetail MM1_SPK_P2P(0);
static constexpr RegDetail MM1_SPLIT_SYNC(1);
static constexpr RegDetail MM1_PR_EOP2DMA(2);
static constexpr RegDetail MM1_SPK_WAIT(16, 23);
static constexpr RegDetail MM1_SYNC2SPK_WAIT(24, 31);

// REGISTER MM2
static constexpr uint32_t REGISTER_MM2 = 0xB4 / 4;
static constexpr RegDetail MM2_SPK_DST_ROW(0, 7);
static constexpr RegDetail MM2_SPK_DST_COL(8, 15);
static constexpr RegDetail MM2_SPK_DST_NP(20, 23);
static constexpr RegDetail MM2_SPK_DST_LAYER(24, 31);

// REGISTER MM3
static constexpr uint32_t REGISTER_MM3 = 0xB8 / 4;
static constexpr RegDetail MM3_FC_DST_ROW(0, 7);
static constexpr RegDetail MM3_FC_DST_COL(8, 15);
static constexpr RegDetail MM3_FC_DST_NP(20, 23);
static constexpr RegDetail MM3_NP_OFF(30);
static constexpr RegDetail MM3_FC_P2P(31);

// REGISTER MM4
static constexpr uint32_t REGISTER_MM4 = 0xBC / 4;
static constexpr RegDetail MM4_EOP_DST_WCOL1(0, 7);
static constexpr RegDetail MM4_EOP_DST_ECOL1(8, 15);
static constexpr RegDetail MM4_EOP_DST_WCOL2(16, 23);
static constexpr RegDetail MM4_EOP_DST_ECOL2(24, 31);

// REGISTER MM5
static constexpr uint32_t REGISTER_MM5 = 0xC0 / 4;
static constexpr RegDetail MM5_LSYNC_DST_WCOL(0, 7);
static constexpr RegDetail MM5_LSYNC_DST_ECOL(8, 15);

// REGISTER MM6
static constexpr uint32_t REGISTER_MM6 = 0xC4 / 4;
static constexpr RegDetail MM6_NPAXI_DST_ROW(0, 7);
static constexpr RegDetail MM6_NPAXI_DST_COL(8, 15);
static constexpr RegDetail MM6_NPAXI_DST_NP(16, 19);
static constexpr RegDetail MM6_NP_ID_2DDR(16, 19);

// REGISTER MM7
static constexpr uint32_t REGISTER_MM7 = 0xC8 / 4;
static constexpr RegDetail MM8_NPDBG_DST_ROW(0, 7);
static constexpr RegDetail MM8_NPDBG_DST_COL(8, 15);
static constexpr RegDetail MM8_NPDBG_DST_NP(16, 19);
static constexpr RegDetail MM8_NPDBG2DDR_EN(31);

// REGISTER MM8
static constexpr uint32_t REGISTER_MM8 = 0xCC / 4;
static constexpr RegDetail MM8_SPK_REPEAT(0, 1);
static constexpr RegDetail MM8_RSPK_DST_NP_3_0(16, 19);
static constexpr RegDetail MM8_RSPK_DST_NP_7_4(20, 23);
static constexpr RegDetail MM8_RSPK_DST_NP_11_8(24, 27);
static constexpr RegDetail MM8_RSPK_DST_NP_15_12(28, 31);

// REGISTER NP_RST
static constexpr uint32_t REGISTER_NP_RST = 0xFC / 4;
static constexpr RegDetail NP_RST_SOFT_RST(0);
static constexpr RegDetail NP_RST_RST_EN(8, 15);

}  // namespace akida
