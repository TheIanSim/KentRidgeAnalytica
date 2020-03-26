from classes import Graph, Node, Simulation

bad_guys=[6,160,51,178]
number_of_timesteps = 100



test_sim = Simulation(bad_guys=bad_guys)
test_sim.load_vertices_from_file("Database 1A.csv", bad_guys)
test_sim.load_edges_from_file("Database 1B.csv")
#test_sim.load_vertices_from_file("Database 1A_test.csv")
#test_sim.load_edges_from_file("Database 1B_test.csv")


for i in range(number_of_timesteps):
    
    if i == 10:
        for v in [4,62,69,110]:
            test_sim.graph.remove_vertex(v)
    

    test_sim.run_one_timestep()
    score_dict = test_sim.graph.get_scores()

    
    test_sim.output.add_timestep_scores(score_dict, i)

test_sim.data_out_to_file("gephi_output4.csv")
