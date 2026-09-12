# Registration checklist

Nothing is reachable until it is registered. Work through both lists.

## lambdapdk repo

- [ ] `lambdapdk/<pdk>/__init__.py` — PDK class + `_<Foo>Path` dataroot mixin.
- [ ] `lambdapdk/<pdk>/libs/*.py` — library classes.
- [ ] `lambdapdk/<pdk>/README.md` — new file. Follow `lambdapdk/icsprout55/README.md`:
      one paragraph on what the release is, the upstream URL, then a `Notes:` list that
      states what is vendored vs fetched, every workaround and why, and **every gap**
      (no DRC deck, no SRAM, estimated RC, unused corners). Add a citation request if
      upstream asks for one (gt2n does).
- [ ] `lambdapdk/__init__.py`:
      - [ ] import the PDK class inside `get_pdks()` and add an instance to the returned set
      - [ ] import each library class inside `get_libs()` and add an instance
      - Every class is instantiated with no arguments; one entry per concrete variant
        (gf180 lists 22 stackup/track combinations, so long lists are normal here).
- [ ] Root `README.md`, four places:
      - [ ] "Supported PDKs" table row (PDK, node, libraries, source)
      - [ ] "Cell Library Inventory" section — a `### <PDK> (<node>)` block with the
            library table and a **Cell categories:** line
      - [ ] "Architecture" tree
      - [ ] License table, if the PDK carries terms beyond Apache 2.0
- [ ] `tests/test_lambdalib_interface.py` — only for new lambdalib memory wrappers.
- [ ] `pyproject.toml` `[tool.tclint] exclude` — only if you vendored upstream Tcl that
      will not pass `tclfmt --check`.

`tests/test_paths.py` and `tests/test_getters.py` parametrize over `get_pdks()` /
`get_libs()` automatically — no edit needed, but they are what catches a missing
registration or a bad path.

## siliconcompiler repo (`~/siliconcompiler`, branch main)

Demo targets live here now, not in lambdapdk. `lambdapdk/<pdk>/target.py` is only a
deprecated forwarding shim for PDKs that once shipped one; a new PDK does not need it.

- [ ] `siliconcompiler/targets/<pdk>_demo.py` — model on `icsprout55_demo.py`:
      `set_mainlib` + `add_asiclib` per library, `set_flow(asicflow.ASICFlow(...))`,
      `add_dep(synflow.SynthesisFlow(...))`, `set_pdk("<name>")`, slow/typical/fast
      scenarios, `set_asic_delaymodel("nldm")`, `area.set_density(...)`,
      `area.set_coremargin(...)`. Keep the numbered comment structure — it is the
      house style and is rendered in the docs.
- [ ] `siliconcompiler/targets/__init__.py` — import and add to `__all__`.
- [ ] `siliconcompiler/targets/_utils.py` — add a branch in `asic_target()` and mention
      the name (and any alias) in its docstring.
- [ ] `tests/targets/test_targets.py` — add to the `parametrize` list.
- [ ] `docs/reference_manual/predef_modules/pdks.rst` — `.. schema::` with
      `:root: lambdapdk.<pdk>/<PDKClass>`
- [ ] `docs/reference_manual/predef_modules/libs.rst` — a `<pdk>` heading plus a
      `.. schema::` per library class
- [ ] `docs/reference_manual/predef_modules/targets.rst` — `.. sctarget::` block
- [ ] `docs/user_guide/include/supported_technologies.inc` — add to the "Open PDKs" row

Corner names must line up across the three files: the scenario's `add_libcorner(name)`
matches `add_asic_libcornerfileset(name, "nldm")` in the library, and its
`set_pexcorner(name)` matches a corner registered on the PDK via `add_pexmodelfileset` /
`add_openroad_rclayer`.

## Gates

```bash
cd /home/pgadfort/lambdapdk && flake8 --statistics . && tclfmt --check . && tclint .
mkdir -p /tmp/lpdk-testrun && cd /tmp/lpdk-testrun && pytest /home/pgadfort/lambdapdk
```

`pytest` here downloads every remote dataroot to check paths — slow, and it needs network.
Run it from a scratch directory, as CI does.
