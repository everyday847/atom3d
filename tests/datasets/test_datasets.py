import pytest
import os
import importlib

import atom3d.datasets as da

# -- Dataset Loaders

def test_load_dataset_lmdb():
    dataset = da.load_dataset('tests/test_data/lmdb', 'lmdb')
    assert len(dataset) == 4

#def test_load_dataset_sharded():
#    dataset = da.load_dataset('tests/test_data/sharded', 'sharded')
#    assert len(dataset) == 4

def test_load_dataset_pdb():
    dataset = da.load_dataset('tests/test_data/pdb', 'pdb')
    assert len(dataset) == 4

def test_load_dataset_sdf():
    dataset = da.load_dataset('tests/test_data/sdf', 'sdf')
    assert len(dataset) == 4

@pytest.mark.skipif(not importlib.util.find_spec("rosetta") is not None,
                    reason="Reading silent files requires pyrosetta!")
def test_load_dataset_silent():
    dataset = da.load_dataset('tests/test_data/silent', 'silent')
    assert len(dataset) == 4

def test_load_dataset_xyz():
    dataset = da.load_dataset('tests/test_data/xyz-gdb', 'xyz')
    assert len(dataset) == 3

def test_load_dataset_xyzgdb():
    file_list = ['tests/test_data/xyz-gdb/dsgdb9nsd_000005.xyz',  
                 'tests/test_data/xyz-gdb/dsgdb9nsd_000212.xyz',  
                 'tests/test_data/xyz-gdb/dsgdb9nsd_001458.xyz']
    dataset = da.load_dataset(file_list, 'xyz-gdb')
    assert len(dataset) == 3


# -- Creator for LMDB dataset

def test_make_lmdb_dataset():
    # Load PDB dataset
    dataset = da.load_dataset('tests/test_data/pdb', 'pdb')
    assert len(dataset) == 4
    # Create LMDB dataset from PDB dataset
    da.make_lmdb_dataset(dataset, 'tests/test_data/_output_lmdb',
                         filter_fn=None, serialization_format='json',
                         include_bonds=False)
    # Try to load generated dataset
    new_dataset = da.load_dataset('tests/test_data/_output_lmdb', 'lmdb')
    assert len(new_dataset) == 4
    # Remove temporary files
    os.remove('tests/test_data/_output_lmdb/data.mdb')
    os.remove('tests/test_data/_output_lmdb/lock.mdb')
    os.rmdir('tests/test_data/_output_lmdb')

