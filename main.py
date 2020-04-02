from classes import Graph, Node, Simulation

bad_guys = [6, 160, 51, 178]
number_of_timesteps = 100

good_guys = [8, 50, 32, 63, 45, 109, 167, 86]
good_guys_enter_timestep = 5
nodes_to_remove = [65, 110]  # 176 reserved for what-if to tip the balance
node_remove_timestep = 15

test_sim = Simulation(
    bad_guys=bad_guys,
    good_guys=good_guys,
    good_guys_enter_timestep=good_guys_enter_timestep,
)
test_sim.load_vertices_from_file("Database 1A.csv", bad_guys)
#test_sim.load_vertices_from_file("removed_central_nodes.csv", bad_guys)
test_sim.load_edges_from_file("Database 1B.csv")
#test_sim.load_edges_from_file("removed_central_edges.csv")



for i in range(number_of_timesteps):
    # for the first timestep, do nothing except log intial scores
    if i > 0:
        score_dict = test_sim.graph.get_scores()
        if i == good_guys_enter_timestep:
            test_sim.graph.set_good_guys(good_guys)

        # good guys remove selected nodes at timestep indicated at node_remove_timestep
        if i == node_remove_timestep:
            for v in nodes_to_remove:
                test_sim.graph.remove_vertex(v)

        test_sim.run_one_timestep(i)

    score_dict = test_sim.graph.get_scores()
    test_sim.output.add_timestep_scores(score_dict, i)

test_sim.data_out_to_file("gephi_output7.csv")
