#!/bin/bash
set -eo pipefail

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export CI=true
export PYTHONHASHSEED=0

# Remove cached results to ensure fresh execution
rm -rf .pytest_cache

pytest -v --tb=short --no-cov -p no:cacheprovider \
    testing/python/arith/ \
    testing/python/transform/ \
    --ignore=testing/python/transform/test_tilelang_transform_cluster_planning.py \
    --ignore=testing/python/transform/test_tilelang_transform_fuse_mbarrier_arrive_expect_tx.py \
    --ignore=testing/python/transform/test_tilelang_transform_hoist_broadcast_values.py \
    --ignore=testing/python/transform/test_tilelang_transform_inject_fence_proxy.py \
    --ignore=testing/python/transform/test_tilelang_transform_layout_inference.py \
    --ignore=testing/python/transform/test_tilelang_transform_lower_hopper_intrin.py \
    --ignore=testing/python/transform/test_tilelang_transform_lower_shared_barrier.py \
    --ignore=testing/python/transform/test_tilelang_transform_multi_version_buffer.py \
    --ignore=testing/python/transform/test_tilelang_transform_pipeline_planning.py \
    --ignore=testing/python/transform/test_tilelang_transform_producer_consumer_ws.py

