cat labels/racism_study.annotated.json | \
python -m jsql/filter query eq "donald trump" | \
# Note: 'n' means 'not actually about racism'
python -m jsql/filter ratings.gcop_v1 neq n | \
python -m graph/pie ratings.gcop_v1 legends/trump_racism
