from game_rule import GameRule

class TestGameRule:
    def test_has_three_line_01(self):
        marks = [" ", "o", "o", "o", " ", " ", "o", "o", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = True
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return

    def test_has_three_line_02(self):
        marks = ["o", " ", "o", "o", " ", "o", " ", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = True
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return

    def test_has_three_line_03(self):
        marks = ["o", "o", " ", "o", " ", "o", "o", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = True
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return

    def test_has_three_line_04(self):
        marks = ["o", " ", "x", "o", "o", " ", "o", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = False
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return

    def test_has_three_line_05(self):
        marks = [" ", "o", "x", "o", "o", " ", " ", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = False
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return

    def test_has_three_line_06(self):
        marks = ["o", "o", " ", "o", " ", " ", " ", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 1
        expected_return = False
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return
        
    def test_has_three_line_07(self):
        marks = ["o", "o", " ", "o", " ", "o", " ", "o", "o"]
        mark = "o"
        # index 1 to 9
        index = 8
        expected_return = False
        assert GameRule()._has_three_line(mark, marks, index)  == expected_return

    def test_has_four_line_01(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", "o", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = True
        assert GameRule()._has_four_line(mark, marks, index)  == expected_return

    def test_has_four_line_02(self):
        marks = ["o", " ", "o", "o", "o", "x", " ", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = True
        assert GameRule()._has_four_line(mark, marks, index)  == expected_return

    def test_has_four_line_03(self):
        marks = ["o", " ", " ", "o", "o", "o", "o", "x", "x"]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = True
        assert GameRule()._has_four_line(mark, marks, index)  == expected_return

    def test_has_four_line_04(self):
        marks = ["o", "o", "x", "o", "o", "x", "o", "o", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = False
        assert GameRule()._has_four_line(mark, marks, index)  == expected_return

    def test_has_four_line_05(self):
        marks = ["x", "o", "o", "o", "o", "x", " ", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = False
        assert GameRule()._has_four_line(mark, marks, index)  == expected_return

    def test_has_four_line_06(self):
        marks = ["o", "o", " ", "o", "x", "o", "o", "o", "o"]
        mark = "o"
        # index 1 to 9
        index = 8
        expected_return = False
        assert GameRule()._has_four_line(mark, marks, index)  == expected_return
        



    def test_get_no_empty_length_01(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", " ", " "]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = 4
        assert GameRule()._get_no_empty_length(index, mark, marks) == expected_return
        
    def test_get_no_empty_length_02(self):
        marks = [" ", " ", "o", "o", " ", "o", "o", "o", "o"]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = 2
        assert GameRule()._get_no_empty_length(index, mark, marks) == expected_return
    
    def test_get_no_empty_length_03(self):
        marks = [" ", " ", " ", "o", " ", "o", "o", "o", "o"]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = 1
        assert GameRule()._get_no_empty_length(index, mark, marks) == expected_return

    def test_get_no_empty_length_04(self):
        marks = ["o", "x", "o", "o", "x", "o", "o", "o", "o"]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = 2
        assert GameRule()._get_no_empty_length(index, mark, marks) == expected_return
        
    def test_get_no_empty_length_05(self):
        marks = ["o", "o", "o", "o", "o", "o", "o", "o", "x"]
        mark = "o"
        # index 1 to 9
        index = 4
        expected_return = 8
        assert GameRule()._get_no_empty_length(index, mark, marks) == expected_return

    def test_get_window_01(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", " ", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 4
        expected_return = [(1, 4),(2,5), (3,6), (4,7)]
        assert GameRule()._get_window_list(marks, index, finding_length) == expected_return

    def test_get_window_02(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", " ", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 2
        expected_return = [(1, 4), (2, 5)]
        assert GameRule()._get_window_list(marks, index, finding_length) == expected_return

    def test_get_window_03(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", "o", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 8
        expected_return = [(5, 8), (6, 9)]
        assert GameRule()._get_window_list(marks, index, finding_length) == expected_return

    def test_get_window_04(self):
        marks = [" ", "x", "o", "o", "o", "x", " ", "o", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 3
        expected_return = [(1, 4), (2, 5), (3, 6)]
        assert GameRule()._get_window_list(marks, index, finding_length) == expected_return

    def test_get_window_05(self):
        marks = [" ", "x", "o", "o", "o", "x", "x", "o", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 8
        expected_return = [(5, 8), (6, 9)]
        assert GameRule()._get_window_list(marks, index, finding_length) == expected_return


    def test_get_windows_01(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", " ", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 4
        expected_return = [(1, 4),(3,6)]
        assert GameRule()._get_windows_with_mark(mark, marks, index, finding_length) == expected_return

    def test_get_windows_02(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", " ", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 2
        expected_return = [(1, 4)]
        assert GameRule()._get_windows_with_mark(mark, marks, index, finding_length) == expected_return

    def test_get_windows_03(self):
        marks = [" ", "o", "o", "o", "o", " ", " ", "o", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 8
        expected_return = []
        assert GameRule()._get_windows_with_mark(mark, marks, index, finding_length) == expected_return

    def test_get_windows_04(self):
        marks = [" ", "x", "o", "o", "o", "x", " ", "o", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 3
        expected_return = [(2, 5), (3, 6)]
        assert GameRule()._get_windows_with_mark(mark, marks, index, finding_length) == expected_return

    def test_get_windows_05(self):
        marks = [" ", "x", "o", "o", "o", "o", "x", "o", " "]
        mark = "o"
        finding_length = 3
        # index 1 to 9
        index = 8
        expected_return = [(5, 8)]
        assert GameRule()._get_windows_with_mark(mark, marks, index, finding_length) == expected_return

    def test_find_index_except_01(self):
        data = [" ", "o", "o", "o"]
        target = "o"
        expected_return = 0
        assert GameRule()._find_index_except(data, target) == expected_return

    def test_find_index_except_02(self):
        data = ["x", "o", "o", "o"]
        target = "o"
        expected_return = 0
        assert GameRule()._find_index_except(data, target) == expected_return

    def test_find_index_except_03(self):
        data = ["o", "o", "o", "o"]
        target = "o"
        expected_return = -1
        assert GameRule()._find_index_except(data, target) == expected_return

    def test_is_both_side_empty_01(self):
        marks = [" ", "o", "o", "o", " ", "o", " ", "o", " "]
        mark = "o"
        left = 1
        right = 4
        window = [" ", "o", "o", "o"]
        expected_return = True
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_02(self):
        marks = ["x", "o", "o", "o", " ", "o", " ", "o", " "]
        mark = "o"
        left = 2
        right = 5
        window = ["o", "o", "o", " "]
        expected_return = False
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_03(self):
        marks = ["x", " ", "o", "o", " ", "o", " ", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", " ", "o"]
        expected_return = True
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_04(self):
        marks = ["x", " ", "o", "o", " ", "o", "x", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", " ", "o"]
        expected_return = False
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_05(self):
        marks = ["x", " ", "o", "o", "x", "o", " ", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", "x", "o"]
        expected_return = False
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_06(self):
        marks = ["x", " ", "o", "o", "o", "x", " ", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", "o", "x"]
        expected_return = False
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_07(self):
        marks = ["o", "o", "o", " ", " ", "o", " ", "o", " "]
        mark = "o"
        left = 1
        right = 4
        window = ["o", "o", "o", " "]
        expected_return = False
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_both_side_empty_08(self):
        marks = ["o", "o", "o", " ", " ", " ", "o", "o", "o"]
        mark = "o"
        left = 6
        right = 9
        window = [" ", "o", "o", "o"]
        expected_return = False
        assert GameRule()._is_both_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_01(self):
        marks = [" ", "o", "o", "o", " ", "o", " ", "o", " "]
        mark = "o"
        left = 1
        right = 4
        window = [" ", "o", "o", "o"]
        expected_return = True
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_02(self):
        marks = ["x", "o", "o", "o", " ", "o", " ", "o", " "]
        mark = "o"
        left = 1
        right = 4
        window = ["x", "o", "o", "o"]
        expected_return = True
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_03(self):
        marks = ["x", "x", "o", "o", " ", "o", " ", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", " ", "o"]
        expected_return = True
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_04(self):
        marks = ["x", "x", "o", "o", " ", "o", "x", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", " ", "o"]
        expected_return = True
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_05(self):
        marks = ["x", "x", "o", "o", "o", " ", "x", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", "o", " "]
        expected_return = True
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_06(self):
        marks = ["x", " ", "o", "o", "x", "o", " ", "o", " "]
        mark = "o"
        left = 3
        right = 6
        window = ["o", "o", "x", "o"]
        expected_return = False
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_07(self):
        marks = ["o", "o", "o", "x", "x", "o", " ", "o", " "]
        mark = "o"
        left = 1
        right = 4
        window = ["o", "o", "o", "x"]
        expected_return = False
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return

    def test_is_single_side_empty_08(self):
        marks = ["o", "o", "o", "x", "x", " ", "o", "o", "o"]
        mark = "o"
        left = 6
        right = 9
        window = [" ", "o", "o", "o"]
        expected_return = True
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return
        
    def test_is_single_side_empty_09(self):
        marks = ["o", "o", "o", "x", "x", "x", "o", "o", "o"]
        mark = "o"
        left = 6
        right = 9
        window = ["x", "o", "o", "o"]
        expected_return = False
        assert GameRule()._is_single_side_empty(left, right, marks, mark) == expected_return
        
    def test_count_elements_in_range_01(self):
        list = ["x", "x", "x", "x", "x", "x"]
        start = 1
        end = 4
        target = "x"
        result = GameRule()._count_elements_in_range(list, start, end, target)
        assert result == 4

    def test_count_elements_in_range_02(self):
        list = ["x", "x", "x", "x", " ", " "]
        start = 1
        end = 4
        target = "x"
        result = GameRule()._count_elements_in_range(list, start, end, target)
        assert result == 4

    def test_count_elements_in_range_03(self):
        list = [" ", "x", "x", "o", " ", " "]
        start = 1
        end = 4
        target = "x"
        result = GameRule()._count_elements_in_range(list, start, end, target)
        assert result == 2
