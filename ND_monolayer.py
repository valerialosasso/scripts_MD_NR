# Run this cell if this notebook is in another folder than the module
import sys, os
sys.path.append("..")
traj_path = os.path.join("/path/to/traj/file", "traj.dcd")
topol_path = os.path.join("/path/to/traj/file", "system.psf")


from md2reflect import *
traj=load_trajectory(traj_path, 
                     filename_topology = os.path.join(topol_path), 
                     skip_frames=1)
zbin_interval, box_zlength, zbins_number, zbin_volume = select_zbinning(traj, 
                                                                        zbin_interval=0.5, 
                                                                        zbins_number=None)
number_atoms_types_allframes = count_number_atoms_types(traj, zbins_number)
number_density_atom_types_allframes = calculate_number_density_atom_types(number_atoms_types_allframes, zbin_volume)

save_number_density_atom_types(number_density_atom_types_allframes, zbin_interval, show=True)

number_atoms_elements_allframes = count_number_atoms(traj, zbins_number)
number_density_elements_allframes = calculate_number_density_elements(number_atoms_elements_allframes, 
                                                                     zbin_volume)
save_number_density(number_density_elements_allframes, zbin_interval, show=True)




