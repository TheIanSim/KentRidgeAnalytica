from classes import Graph, Node, Simulation

bad_guys=[6,160,51,178]
number_of_timesteps = 100

good_guys = []
good_guys_enter_timestep = 10
nodes_to_remove = [4,62,69,110] 



test_sim = Simulation(bad_guys=bad_guys)
test_sim.load_vertices_from_file("Database 1A.csv", bad_guys)
test_sim.load_edges_from_file("Database 1B.csv")
#test_sim.load_vertices_from_file("Database 1A_test.csv")
#test_sim.load_edges_from_file("Database 1B_test.csv")


for i in range(number_of_timesteps):
    #for the first timestep, do nothing except log intial scores
    if i > 0:
        score_dict = test_sim.graph.get_scores()
        
        #good guys remove selected nodes at timestep 10
        if i == 10:
            for v in nodes_to_remove :
                test_sim.graph.remove_vertex(v)
        

        test_sim.run_one_timestep()
    
    score_dict = test_sim.graph.get_scores()    
    test_sim.output.add_timestep_scores(score_dict, i)

test_sim.data_out_to_file("gephi_output5.csv")
