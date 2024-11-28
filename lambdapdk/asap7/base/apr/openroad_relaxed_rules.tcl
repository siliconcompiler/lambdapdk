utl::warn FLW 1 "Relaxed technology routing rules loaded for ASAP7,\
    this should only be used for trial routing"

utl::info FLW 1 "Removing right way on grid only rules"
[[ord::get_db_tech] findLayer M1] setRightWayOnGridOnly 0
[[ord::get_db_tech] findLayer M2] setRightWayOnGridOnly 0
[[ord::get_db_tech] findLayer M3] setRightWayOnGridOnly 0
[[ord::get_db_tech] findLayer M4] setRightWayOnGridOnly 0
[[ord::get_db_tech] findLayer M5] setRightWayOnGridOnly 0
[[ord::get_db_tech] findLayer M6] setRightWayOnGridOnly 0
[[ord::get_db_tech] findLayer M7] setRightWayOnGridOnly 0
