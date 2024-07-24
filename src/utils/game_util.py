
from models.game_objects import Card

class HandScoringUtil:
    
    # Sorting
    def merge_sort(array: list) -> None:
        if len(array) < 2:
            return
        
        midpoint = int(len(array) / 2)
        left = array[:midpoint]
        right = array[midpoint:]
        
        HandScoringUtil.merge_sort(left)
        HandScoringUtil.merge_sort(right)
        
        HandScoringUtil.merge(array, left, right)

    def merge(array: list, left: list, right: list) -> None:
        i = 0
        while True:
            if len(left) + len(right) == 0:
                break
            try:
                if left[0] < right[0]:
                    array[i] = left.pop(0)
                else:
                    array[i] = right.pop(0)
            except:
                if len(left) == 0:
                    array[i] = right.pop(0)
                else:
                    array[i] = left.pop(0)
            i += 1

    def sort_out_faces(array: list[Card]) -> dict:
        sorted_cards = {'c': [], 'd': [], 'h': [], 's': []}
        for card in array:
            sorted_cards[card.get_face()].append(card)

        return sorted_cards

    def walk_array(array: list[Card], size: int):
        '''
        Given an array, return sets of "size" cards
        starting from the last element backwards
        '''
        HandScoringUtil.merge_sort(array)
        arrays = []
        length = len(array) - (size - 1)
        for i in range(length):
            start = (i+size) * -1
            stop = i * -1
            if i == 0:
                arrays.append(array[start:])
            else:
                arrays.append(array[start:stop])
        return arrays
                
    # Scoring
    def score_simple(card_score: int, tier: int) -> int:
        '''
        Returns the card score: 1-13
        '''
        return round(((card_score / 13) * 100) + (tier * 100), 2)
    
    def score_bidir(card_score: tuple[int,int], tier: int) -> int:
        smaller, larger = card_score
        return (((larger / 13) * 100) + (smaller/13)) + (tier * 100)

    def is_straight(array: list[Card]) -> int:
        '''
        Takes list[Card] with length of 5
        returns -1 if array does not represent
        a straight
        returns last element in array if
        it represents a straight
        '''
        HandScoringUtil.merge_sort(array)
        edge_array = list(set(array))
        if edge_array[-1] - edge_array[3] == 9:
            return edge_array[3].get_points_value()
        
        values_range = array[-1] - array[0]

        if values_range == 4:
            if len(set(array)) == 5:
                return array[-1].get_points_value()

        return 0
    
    def is_flush(array: list[Card]) -> int:
        '''
        Takes an array of 5 Card(s)
        returns -1 if not flush, otherwise
        '''
        HandScoringUtil.merge_sort(array)
        for card in array:
            if card.get_face() != array[0].get_face():
                return 0

        return array[-1].get_points_value()
    
    def is_multiple(array: list[Card], amount: int) -> int:
        HandScoringUtil.merge_sort(array)
        searches = HandScoringUtil.walk_array(array, amount)

        for search in searches:
            if len(set(search)) == 1:
                score = search[0].get_points_value()
                return score
        return 0

    def get_multiples(array: list[Card], amount: int) -> list[int]:
        HandScoringUtil.merge_sort(array)
        searches = HandScoringUtil.walk_array(array, amount)
        scores = []
        for search in searches:
            if len(set(search)) == 1:
                score = search[0].get_points_value()
                scores.append(score)
        return scores

    def score_high_card(array: list[Card]):
        
        return HandScoringUtil.score_simple()

    def score_pair(array: list[Card]):
        pair = HandScoringUtil.is_multiple(array, 2)
        if pair:
            return HandScoringUtil.score_simple(pair, 1)

    def score_three_oak(array: list[Card]) -> int:
        three_oak = HandScoringUtil.is_multiple(array, 3)
        if three_oak:
            return HandScoringUtil.score_simple(three_oak, 3)
        return 0
    
    def score_flush(array: list[Card]) -> int:
        for quintet in HandScoringUtil.walk_array(array, 5):
            is_flush = HandScoringUtil.is_flush(quintet)
            if is_flush:
                return HandScoringUtil.score_simple(is_flush, 5)
        return 0

    def score_full_house(array: list[Card]) -> int:
        # check for pair & 3 of a kind
        # return bidir(lowcard, highcard)
        three_oak = HandScoringUtil.is_multiple(array, 3)
        pair_multiples = HandScoringUtil.get_multiples(array, 2)

        if len(pair_multiples) == 0 or three_oak == 0:
            return 0

        for multiple in pair_multiples:
            if multiple != three_oak:
                pair = multiple
                break

        if three_oak != pair:
            return HandScoringUtil.score_bidir([pair, three_oak], 6)
        return 0

    def score_four_oak(array: list[Card]) -> int:
        four_oak = HandScoringUtil.is_multiple(array, 4)
        if four_oak:
            return HandScoringUtil.score_simple(four_oak, 7)
        return 0

    def score_straight_flush(array: list[Card]) -> int:
        HandScoringUtil.merge_sort(array)
        sep_array = HandScoringUtil.sort_out_faces(array)
        for face in sep_array.keys():
            array = sep_array[face]
            if len(array) >= 5:
                for array in HandScoringUtil.walk_array(array, 5):
                    straight_score = HandScoringUtil.is_straight(array)
                    if straight_score:
                        return HandScoringUtil.score_simple(straight_score, 8)
        return 0
    
    def score_royal_flush(array: list[Card]) -> int:
        HandScoringUtil.merge_sort(array)
        sep_array = HandScoringUtil.sort_out_faces(array)
        for face in sep_array.keys():
            array = sep_array[face]
            if len(array) >= 5:
                straight_score = HandScoringUtil.is_straight(array)
                return 1000
        return 0
    
    def calculate_score(array: list[Card]):
        rf_score = HandScoringUtil.score_royal_flush(array)
        sf_score = HandScoringUtil.score_straight_flush(array)
        foak_score = HandScoringUtil.score_four_oak(array)
        fh_score = HandScoringUtil.score_full_house(array)
        flush_score = HandScoringUtil.score_flush(array)
        toak_score = HandScoringUtil.score_three_oak(array)
        pair_score = HandScoringUtil.score_pair(array)



        if rf_score:
            return rf_score
        if sf_score:
            return sf_score
        if foak_score:
            return foak_score
        if fh_score:
            return fh_score
        if flush_score:
            return flush_score
        if toak_score:
            return toak_score
        if pair_score:
            return pair_score

        return 0