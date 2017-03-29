import os.path as p

import numpy as np
import matplotlib.pyplot as plt

self_path = p.dirname(p.abspath(__file__))
root_path = p.dirname(self_path)

import sys
sys.path.append(p.join(root_path, 'test'))
import output_preservation_test as opt


grid_points = np.array([10, 20, 40, 60, 80, 100, 150, 200, 300, 400, 500])

def benchmark_gaussian_bump_red_grav():
    run_time_O1 = np.zeros(len(grid_points))
    run_time_Ofast = np.zeros(len(grid_points))

    with opt.working_directory(p.join(self_path, "beta_plane_bump_red_grav")):
        aro_exec = "aronnax_test"
        for counter, nx in enumerate(grid_points):
            run_time_O1[counter] = opt.run_experiment(
                opt.write_input_beta_plane_bump_red_grav, nx, nx, 1, aro_exec)

        aro_exec = "aronnax_core"
        for counter, nx in enumerate(grid_points):
            run_time_Ofast[counter] = opt.run_experiment(
                opt.write_input_beta_plane_bump_red_grav, nx, nx, 1, aro_exec)

        plt.figure()
        plt.plot(grid_points, run_time_O1, '-*', label='Aronnax run time -O1')
        plt.plot(grid_points, run_time_Ofast,
            '-*', label='Aronnax run time -Ofast')
        plt.plot(grid_points,
            (run_time_O1[-7]/(grid_points[-7]**2))*grid_points**2,
            '-*', label='O(nx*nx)')
        plt.legend()
        plt.xlabel('nx')
        plt.ylabel('run time (s) for 502 timesteps')
        plt.savefig('beta_plane_bump_red_grav scaling.png', dpi=150)


def benchmark_gaussian_bump():
    run_time_O1 = np.zeros(len(grid_points))
    run_time_Ofast = np.zeros(len(grid_points))
    run_time_hypre_test = np.zeros(len(grid_points))
    run_time_hypre = np.zeros(len(grid_points))

    with opt.working_directory(p.join(self_path, "beta_plane_bump")):

        aro_exec = "aronnax_test"
        for counter, nx in enumerate(grid_points[:8]):
            run_time_O1[counter] = opt.run_experiment(
                  opt.write_input_beta_plane_bump, nx, nx, 2, aro_exec)

        aro_exec = "aronnax_core"
        for counter, nx in enumerate(grid_points[:8]):
            run_time_Ofast[counter] = opt.run_experiment(
                  opt.write_input_beta_plane_bump, nx, nx, 2, aro_exec)

        aro_exec = "aronnax_external_solver_test"
        for counter, nx in enumerate(grid_points[:9]):
            run_time_hypre_test[counter] = opt.run_experiment(
                  opt.write_input_beta_plane_bump, nx, nx, 2, aro_exec)

        aro_exec = "aronnax_external_solver"
        for counter, nx in enumerate(grid_points[:9]):
            run_time_hypre[counter] = opt.run_experiment(
                  opt.write_input_beta_plane_bump, nx, nx, 2, aro_exec)

        plt.figure()
        plt.plot(grid_points[:8], run_time_O1[:8],
            '-*', label='Aronnax run time -O1')
        plt.plot(grid_points[:8], run_time_Ofast[:8], '-*',
            label='Aronnax run time -Ofast')
        plt.plot(grid_points[:9], run_time_hypre_test[:9], '-*',
            label='Aronnax run time Hypre test')
        plt.plot(grid_points[:9], run_time_hypre[:9], '-*',
            label='Aronnax run time Hypre -Ofast')
        plt.plot(grid_points[:9],
            (run_time_O1[-6]/(grid_points[-6]**2))*grid_points[:9]**2,
            '-*', label='O(nx**2)')
        plt.plot(grid_points[:8],
            (run_time_O1[-6]/(grid_points[-6]**3))*grid_points[:8]**3,
            '-*', label='O(nx**3)')
        plt.legend()
        plt.xlabel('nx')
        plt.ylabel('run time (s) for 502 timesteps')
        plt.savefig('beta_plane_bump scaling.png', dpi=150)

if __name__ == '__main__':
    benchmark_gaussian_bump_red_grav()
    benchmark_gaussian_bump()
