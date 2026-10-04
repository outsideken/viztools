# viztools compatibility

`viztools` versions **independently** of jematools, wherewhen, h3tools and
tabtools. To avoid copies that go stale, this file states no version numbers.
Each fact lives in one place:

| Fact | Where it lives |
|---|---|
| This package's version | `viztools/_version.py` (`viztools.__version__`); history in [CHANGELOG.md](CHANGELOG.md) |
| What viztools requires | `dependencies` and `requires-python` in `pyproject.toml` |
| What other packages require of viztools | each package's own `pyproject.toml` |
| Behaviour consumers can rely on | [VIZTOOLS_CONTRACT.md](VIZTOOLS_CONTRACT.md) |
| Tested combinations and the current freeze | the toolkit matrix: `COMPATIBILITY.md` in the private workspace repo outsideken/geo-toolkit (`../COMPATIBILITY.md` in the workspace checkout) |

## Release checklist

1. Bump `viztools/_version.py`, the only place the version is typed
   (`pyproject.toml` reads it; `tests/test_one_version.py` fails if a copy
   appears elsewhere).
2. Move the `[Unreleased]` section of `CHANGELOG.md` to the new version, dated.
3. Update `VIZTOOLS_CONTRACT.md` if the public contract changes. It states no
   version numbers, so a release that changes no behaviour leaves it alone.
4. After the release PR merges: tag `viztools-vX.Y.Z`.
5. Once the stack is verified, update the toolkit matrix in outsideken/geo-toolkit
   (current-freeze table and a dated row).
6. Bump a dependant's floor only when it starts calling new APIs, then re-test
   the stack.
