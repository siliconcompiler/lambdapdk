# The tap cell is the sole BPR riser per row in this backside-PDN
# configuration, so tap density directly sets BPR rail resistance and
# IR drop -- tighter spacing matters more than in a conventional
# well-tap-only flow. Two microns gives a few tap columns even on
# small blocks.
tapcell \
    -distance 2 \
    -tapcell_master gt2_6t_tapbspdn_w13_svt \
    -endcap_master gt2_6t_tapbspdn_w13_svt
