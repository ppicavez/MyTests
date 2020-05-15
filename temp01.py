i_search = begin
            while not found:
                while not found and i_search <end:
                    i_dir = 0
                    while not found and i_dir < 4:
                
                        current_square = adjacents_squares[i_search][2 * i_dir]
                        if current_square != -1 :
                            if current_square in squares_not_explored and 
                                not in  checked_square : #pour éviter de retourner en arrière
                                found = True
                                found_square = current_square
                            else :    
                                checked_square.append(current_square)
                                i_dir = i_dir +1  
                        else :
                            i_search = i_search + 1

                    begin = end -1
                    end = len(checked_square)






            #Recherche dans les pastilles restantes de la grille              
            #On affecte soit la pastille la plus proche
            # (to do ) Soit une pastille pour répartir les pacs pour couvrir le plus de terrain possible 
        
        if not pacs_affectation[n_pac] :
            print("Passage"  , file=sys.stderr)
            
            checked_square = []
            adjacentes= adjacents_squares[n_square]
            found = False
            i_dir = 0
            while not found and i_dir < 4:
                current_square = adjacents_squares[n_square][2 * i_dir]
                if current_square != -1 :
                    if current_square in squares_not_explored :
                        found = True
                        found_square = current_square
                    else :    
                        checked_square.append(current_square)
                        i_dir = i_dir +1
            begin = 0
            end = len(checked_square)