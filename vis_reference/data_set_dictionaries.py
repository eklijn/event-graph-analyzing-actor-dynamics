node_properties = {}
abbr_dict = {}
events_to_merge = {}
action_encoding = {}
encoding_to_abbr = {}
cluster_descriptions = {}
abbr_dict_lpm = {}

node_properties["bpic2017"] = {
    "A_Accepted+COMPLETE": ["square", "0.3", "0.3", "#8dd3c7"],
    "A_Cancelled+COMPLETE": ["square", "0.3", "0.3", "#ffffb3"],
    "A_Complete+COMPLETE": ["square", "0.3", "0.3", "#d9d9d9"],
    "A_Concept+COMPLETE": ["square", "0.3", "0.3", "#fb8072"],
    "A_Create Application+COMPLETE": ["square", "0.3", "0.3", "#fdb462"],
    "A_Denied+COMPLETE": ["square", "0.3", "0.3", "#80b1d3"],
    "A_Incomplete+COMPLETE": ["square", "0.3", "0.3", "#b3de69"],
    "A_Pending+COMPLETE": ["square", "0.3", "0.3", "#fccde5"],
    "A_Submitted+COMPLETE": ["square", "0.3", "0.3", "#bebada"],
    "A_Validating+COMPLETE": ["square", "0.3", "0.3", "#bc80bd"],
    "O_Accepted+COMPLETE": ["circle", "0.3", "0.3", "#1b9e77"],
    "O_Cancelled+COMPLETE": ["circle", "0.3", "0.3", "#e6ab02"],
    "O_Create Offer+COMPLETE": ["circle", "0.3", "0.3", "#d95f02"],
    "O_Created+COMPLETE": ["circle", "0.3", "0.3", "#7570b3"],
    "O_Refused+COMPLETE": ["circle", "0.3", "0.3", "#66a61e"],
    "O_Returned+COMPLETE": ["circle", "0.3", "0.3", "#e7298a"],
    "O_Sent (mail and online)+COMPLETE": ["circle", "0.3", "0.3", "#a6761d"],
    "O_Sent (online only)+COMPLETE": ["circle", "0.3", "0.3", "#666666"],
    "W_Assess potential fraud+SCHEDULE": ["rect", "0.15", "0.3", "#feedde"],
    "W_Assess potential fraud+START": ["rect", "0.15", "0.3", "#fdbe85"],
    "W_Assess potential fraud+WITHDRAW": ["rect", "0.15", "0.3", "#fd8d3c"],
    "W_Assess potential fraud+ATE_ABORT": ["rect", "0.15", "0.3", "#e6550d"],
    "W_Assess potential fraud+COMPLETE": ["rect", "0.15", "0.3", "#a63603"],
    "W_Call after offers+SCHEDULE": ["rect", "0.15", "0.3", "#eff3ff"],
    "W_Call after offers+START": ["rect", "0.15", "0.3", "#bdd7e7"],
    "W_Call after offers+WITHDRAW": ["rect", "0.15", "0.3", "#6baed6"],
    "W_Call after offers+ATE_ABORT": ["rect", "0.15", "0.3", "#3182bd"],
    "W_Call after offers+COMPLETE": ["rect", "0.15", "0.3", "#08519c"],
    "W_Call incomplete files+SCHEDULE": ["rect", "0.15", "0.3", "#fee5d9"],
    "W_Call incomplete files+START": ["rect", "0.15", "0.3", "#fcae91"],
    "W_Call incomplete files+ATE_ABORT": ["rect", "0.15", "0.3", "#de2d26"],
    "W_Call incomplete files+COMPLETE": ["rect", "0.15", "0.3", "#a50f15"],
    "W_Complete application+SCHEDULE": ["rect", "0.15", "0.3", "#edf8e9"],
    "W_Complete application+START": ["rect", "0.15", "0.3", "#bae4b3"],
    "W_Complete application+WITHDRAW": ["rect", "0.15", "0.3", "#74c476"],
    "W_Complete application+ATE_ABORT": ["rect", "0.15", "0.3", "#31a354"],
    "W_Complete application+COMPLETE": ["rect", "0.15", "0.3", "#006d2c"],
    "W_Handle leads+SCHEDULE": ["rect", "0.15", "0.3", "#f7f7f7"],
    "W_Handle leads+START": ["rect", "0.15", "0.3", "#cccccc"],
    "W_Handle leads+WITHDRAW": ["rect", "0.15", "0.3", "#969696"],
    "W_Handle leads+ATE_ABORT": ["rect", "0.15", "0.3", "#636363"],
    "W_Handle leads+COMPLETE": ["rect", "0.15", "0.3", "#252525"],
    "W_Personal Loan collection+SCHEDULE": ["rect", "0.15", "0.3", "#80cdc1"],
    "W_Personal Loan collection+START": ["rect", "0.15", "0.3", "#018571"],
    "W_Shortened completion +SCHEDULE": ["rect", "0.15", "0.3", "#dfc27d"],
    "W_Shortened completion +START": ["rect", "0.15", "0.3", "#a6611a"],
    "W_Validate application+SCHEDULE": ["rect", "0.15", "0.3", "#f2f0f7"],
    "W_Validate application+START": ["rect", "0.15", "0.3", "#cbc9e2"],
    "W_Validate application+ATE_ABORT": ["rect", "0.15", "0.3", "#756bb1"],
    "W_Validate application+COMPLETE": ["rect", "0.15", "0.3", "#54278f"]
}

abbr_dict["bpic2017"] = {
    "A_Create Application+COMPLETE": "<<B>A<SUB>0</SUB></B>>",
    "A_Submitted+COMPLETE": "<<B>A<SUB>1</SUB></B>>",
    "A_Concept+COMPLETE": "<<B>A<SUB>2</SUB></B>>",
    "A_Accepted+COMPLETE": "<<B>A<SUB>3</SUB></B>>",
    "A_Complete+COMPLETE": "<<B>A<SUB>4</SUB></B>>",
    "A_Validating+COMPLETE": "<<B>A<SUB>5</SUB></B>>",
    "A_Incomplete+COMPLETE": "<<B>A<SUB>6</SUB></B>>",
    "A_Denied+COMPLETE": "<<B>A<SUB>7</SUB></B>>",
    "A_Pending+COMPLETE": "<<B>A<SUB>8</SUB></B>>",
    "A_Cancelled+COMPLETE": "<<B>A<SUB>9</SUB></B>>",
    "O_Create Offer+COMPLETE": "<<B>O<SUB>0</SUB></B>>",
    "O_Created+COMPLETE": "<<B>O<SUB>1</SUB></B>>",
    "O_Sent (mail and online)+COMPLETE": "<<B>O<SUB>2</SUB></B>>",
    "O_Sent (online only)+COMPLETE": "<<B>O<SUB>3</SUB></B>>",
    "O_Returned+COMPLETE": "<<B>O<SUB>4</SUB></B>>",
    "O_Refused+COMPLETE": "<<B>O<SUB>5</SUB></B>>",
    "O_Accepted+COMPLETE": "<<B>O<SUB>6</SUB></B>>",
    "O_Cancelled+COMPLETE": "<<B>O<SUB>7</SUB></B>>",
    "W_Assess potential fraud+SCHEDULE": "<<B>F<SUB>1</SUB></B>>",
    "W_Assess potential fraud+START": "<<B>F<SUB>2</SUB></B>>",
    "W_Assess potential fraud+WITHDRAW": "<<B>F<SUB>3</SUB></B>>",
    "W_Assess potential fraud+ATE_ABORT": "<<B>F<SUB>4</SUB></B>>",
    "W_Assess potential fraud+COMPLETE": "<<B>F<SUB>5</SUB></B>>",
    "W_Call after offers+SCHEDULE": "<<B>C<SUB>1</SUB></B>>",
    "W_Call after offers+START": "<<B>C<SUB>2</SUB></B>>",
    "W_Call after offers+WITHDRAW": "<<B>C<SUB>3</SUB></B>>",
    "W_Call after offers+ATE_ABORT": "<<B>C<SUB>4</SUB></B>>",
    "W_Call after offers+COMPLETE": "<<B>C<SUB>5</SUB></B>>",
    "W_Call incomplete files+SCHEDULE": "<<B>I<SUB>1</SUB></B>>",
    "W_Call incomplete files+START": "<<B>I<SUB>2</SUB></B>>",
    "W_Call incomplete files+ATE_ABORT": "<<B>I<SUB>4</SUB></B>>",
    "W_Call incomplete files+COMPLETE": "<<B>I<SUB>5</SUB></B>>",
    "W_Complete application+SCHEDULE": "<<B>W<SUB>1</SUB></B>>",
    "W_Complete application+START": "<<B>W<SUB>2</SUB></B>>",
    "W_Complete application+WITHDRAW": "<<B>W<SUB>3</SUB></B>>",
    "W_Complete application+ATE_ABORT": "<<B>W<SUB>4</SUB></B>>",
    "W_Complete application+COMPLETE": "<<B>W<SUB>5</SUB></B>>",
    "W_Handle leads+SCHEDULE": "<<B>H<SUB>1</SUB></B>>",
    "W_Handle leads+START": "<<B>H<SUB>2</SUB></B>>",
    "W_Handle leads+WITHDRAW": "<<B>H<SUB>3</SUB></B>>",
    "W_Handle leads+ATE_ABORT": "<<B>H<SUB>4</SUB></B>>",
    "W_Handle leads+COMPLETE": "<<B>H<SUB>5</SUB></B>>",
    "W_Personal Loan collection+SCHEDULE": "<<B>P<SUB>1</SUB></B>>",
    "W_Personal Loan collection+START": "<<B>P<SUB>2</SUB></B>>",
    "W_Shortened completion +SCHEDULE": "<<B>S<SUB>1</SUB></B>>",
    "W_Shortened completion +START": "<<B>S<SUB>2</SUB></B>>",
    "W_Validate application+SCHEDULE": "<<B>V<SUB>1</SUB></B>>",
    "W_Validate application+START": "<<B>V<SUB>2</SUB></B>>",
    "W_Validate application+ATE_ABORT": "<<B>V<SUB>4</SUB></B>>",
    "W_Validate application+COMPLETE": "<<B>V<SUB>5</SUB></B>>"
}

abbr_dict_lpm["bpic2017"] = {
    "A_Create Application+COMPLETE": "A_Cr app+C",
    "A_Submitted+COMPLETE": "A_Subm+C",
    "A_Concept+COMPLETE": "A_Conc+C",
    "A_Accepted+COMPLETE": "A_Acc+C",
    "A_Complete+COMPLETE": "A_Compl app+C",
    "A_Validating+COMPLETE": "A_Val+C",
    "A_Incomplete+COMPLETE": "A_Inc+C",
    "A_Denied+COMPLETE": "A_Denied+C",
    "A_Pending+COMPLETE": "A_Pend+C",
    "A_Cancelled+COMPLETE": "A_Canc+C",
    "O_Create Offer+COMPLETE": "O_Cr off+C",
    "O_Created+COMPLETE": "O_Crtd+C",
    "O_Sent (mail and online)+COMPLETE": "O_Sent mo+C",
    "O_Sent (online only)+COMPLETE": "O_Sent o+C",
    "O_Returned+COMPLETE": "O_Ret+C",
    "O_Refused+COMPLETE": "O_Ref+C",
    "O_Accepted+COMPLETE": "O_Acc+C",
    "O_Cancelled+COMPLETE": "O_Canc+C",
    "W_Assess potential fraud+SCHEDULE": "W_Ass pf+H",
    "W_Assess potential fraud+START": "W_Ass pf+S",
    "W_Assess potential fraud+WITHDRAW": "W_Ass pf+W",
    "W_Assess potential fraud+ATE_ABORT": "W_Ass pf+A",
    "W_Assess potential fraud+COMPLETE": "W_Ass pf+C",
    "W_Call after offers+SCHEDULE": "W_Call off+H",
    "W_Call after offers+START": "W_Call off+S",
    "W_Call after offers+WITHDRAW": "W_Call off+W",
    "W_Call after offers+ATE_ABORT": "W_Call off+A",
    "W_Call after offers+COMPLETE": "W_Call off+C",
    "W_Call incomplete files+SCHEDULE": "W_Call inc+H",
    "W_Call incomplete files+START": "W_Call inc+S",
    "W_Call incomplete files+ATE_ABORT": "W_Call inc+A",
    "W_Call incomplete files+COMPLETE": "W_Call inc+C",
    "W_Complete application+SCHEDULE": "W_Compl app+H",
    "W_Complete application+START": "W_Compl app+S",
    "W_Complete application+WITHDRAW": "W_Compl app+W",
    "W_Complete application+ATE_ABORT": "W_Compl app+A",
    "W_Complete application+COMPLETE": "W_Compl app+C",
    "W_Handle leads+SCHEDULE": "W_Hndl lds+H",
    "W_Handle leads+START": "W_Hndl lds+S",
    "W_Handle leads+WITHDRAW": "W_Hndl lds+W",
    "W_Handle leads+ATE_ABORT": "W_Hndl lds+A",
    "W_Handle leads+COMPLETE": "W_Hndl lds+C",
    "W_Personal Loan collection+SCHEDULE": "W_Pers lc+H",
    "W_Personal Loan collection+START": "W_Pers lc+S",
    "W_Shortened completion +SCHEDULE": "W_Short compl+H",
    "W_Shortened completion +START": "W_Short compl+S",
    "W_Validate application+SCHEDULE": "W_Val app+H",
    "W_Validate application+START": "W_Val app+S",
    "W_Validate application+ATE_ABORT": "W_Val app+A",
    "W_Validate application+COMPLETE": "W_Val app+C"
}

events_to_merge["bpic2017"] = [
    [["O_Sent (mail and online)+COMPLETE", "O_Sent (online only)+COMPLETE"], "O_Sent+COMPLETE"],
    [["W_Call after offers+ATE_ABORT", "W_Call after offers+WITHDRAW"], "W_Call after offers+END"],
    [["W_Call incomplete files+ATE_ABORT", "W_Call incomplete files+COMPLETE"], "W_Call incomplete files+END"],
    [["W_Complete application+WITHDRAW", "W_Complete application+ATE_ABORT", "W_Complete application+COMPLETE"],
     "W_Complete application+END"],
    [["W_Handle leads+WITHDRAW", "W_Handle leads+ATE_ABORT", "W_Handle leads+COMPLETE"], "W_Handle leads+END"],
    [["W_Validate application+ATE_ABORT", "W_Validate application+COMPLETE"], "W_Validate application+END"]
]

action_encoding["bpic2017"] = {
    "A_Accepted+COMPLETE": "A",
    "A_Cancelled+COMPLETE": "B",
    "A_Complete+COMPLETE": "C",
    "A_Concept+COMPLETE": "D",
    "A_Create Application+COMPLETE": "E",
    "A_Denied+COMPLETE": "F",
    "A_Incomplete+COMPLETE": "G",
    "A_Pending+COMPLETE": "H",
    "A_Submitted+COMPLETE": "I",
    "A_Validating+COMPLETE": "J",
    "O_Accepted+COMPLETE": "K",
    "O_Cancelled+COMPLETE": "L",
    "O_Create Offer+COMPLETE": "M",
    "O_Created+COMPLETE": "N",
    "O_Refused+COMPLETE": "O",
    "O_Returned+COMPLETE": "P",
    "O_Sent (mail and online)+COMPLETE": "Q",
    "O_Sent (online only)+COMPLETE": "R",
    "W_Assess potential fraud+SCHEDULE": "S",
    "W_Assess potential fraud+START": "T",
    "W_Assess potential fraud+WITHDRAW": "U",
    "W_Assess potential fraud+ATE_ABORT": "V",
    "W_Assess potential fraud+COMPLETE": "W",
    "W_Call after offers+SCHEDULE": "X",
    "W_Call after offers+START": "Y",
    "W_Call after offers+WITHDRAW": "Z",
    "W_Call after offers+ATE_ABORT": "a",
    "W_Call after offers+COMPLETE": "b",
    "W_Call incomplete files+SCHEDULE": "c",
    "W_Call incomplete files+START": "d",
    "W_Call incomplete files+ATE_ABORT": "e",
    "W_Call incomplete files+COMPLETE": "f",
    "W_Complete application+SCHEDULE": "g",
    "W_Complete application+START": "h",
    "W_Complete application+WITHDRAW": "i",
    "W_Complete application+ATE_ABORT": "j",
    "W_Complete application+COMPLETE": "k",
    "W_Handle leads+SCHEDULE": "l",
    "W_Handle leads+START": "m",
    "W_Handle leads+WITHDRAW": "n",
    "W_Handle leads+ATE_ABORT": "o",
    "W_Handle leads+COMPLETE": "p",
    "W_Personal Loan collection+SCHEDULE": "q",
    "W_Personal Loan collection+START": "r",
    "W_Shortened completion +SCHEDULE": "s",
    "W_Shortened completion +START": "t",
    "W_Validate application+SCHEDULE": "u",
    "W_Validate application+START": "v",
    "W_Validate application+ATE_ABORT": "w",
    "W_Validate application+COMPLETE": "x"
}

encoding_to_abbr["bpic2017"] = {
    "A": "$A_3$",
    "B": "$A_9$",
    "C": "$A_4$",
    "D": "$A_2$",
    "E": "$A_0$",
    "F": "$A_7$",
    "G": "$A_6$",
    "H": "$A_8$",
    "I": "$A_1$",
    "J": "$A_5$",
    "K": "$O_6$",
    "L": "$O_7$",
    "M": "$O_0$",
    "N": "$O_1$",
    "O": "$O_5$",
    "P": "$O_4$",
    "Q": "$O_2$",
    "R": "$O_3$",
    "S": "$F_1$",
    "T": "$F_2$",
    "U": "$F_3$",
    "V": "$F_4$",
    "W": "$F_5$",
    "X": "$C_1$",
    "Y": "$C_2$",
    "Z": "$C_3$",
    "a": "$C_4$",
    "b": "$C_5$",
    "c": "$I_1$",
    "d": "$I_2$",
    "e": "$I_4$",
    "f": "$I_5$",
    "g": "$W_1$",
    "h": "$W_2$",
    "i": "$W_3$",
    "j": "$W_4$",
    "k": "$W_5$",
    "l": "$H_1$",
    "m": "$H_2$",
    "n": "$H_3$",
    "o": "$H_4$",
    "p": "$H_5$",
    "q": "$P_1$",
    "r": "$P_2$",
    "s": "$S_1$",
    "t": "$S_2$",
    "u": "$V_1$",
    "v": "$V_2$",
    "w": "$V_4$",
    "x": "$V_5$"
}

cluster_descriptions["bpic2017"] = {"start": "start",
                                    "end": "end",
                                    0: "[0]\n(A)Accept, (O)Create,\n(W)Call offers-start, (A)Complete",
                                    1: "[1]\n(A)Create, (A)Concept",
                                    2: "[2]\n(A)Create, (A)Submit\n(W)Handle Lds-start",
                                    3: "",
                                    4: "[4]\n(O)Accept, (A)Pending,\n(W)Call inc/Validate-end",
                                    5: "[5]\n(A)Create, (A)Concept\n(A)Accept, (O)Create\n"
                                       "(W)Call offers-start, (A)Complete",
                                    6: "",
                                    7: "[7]\n(A)Denied, (O)Refused\n(W)Call inc/Validate-end",
                                    8: "[8]\n(W)Call offers/Call inc-start\n(W)Validate-start, (A)Validating\n"
                                       "(W)Validate-end, (W)Call inc-start\n(A)Incomplete",
                                    9: "[9]\n(O)Create",
                                    10: "[10]\n(A)Create, (A)Concept\n(A)Accept, (O)Create\n"
                                        "(W)Call offers-start, (A)Complete\n(W)Validate, (A)Validating\n"
                                        "(W)Call inc, (A)Incomplete",
                                    11: "[11]\n(W)Validate-end, (W)Call inc-start,\n(A)Incomplete",
                                    12: "[12]\n(A)Cancel, (O)Cancel\n(W)Call inc/Validate-end",
                                    13: "[13]\n(W)Handle Lds-end, (W)Complete appl-start\n(A)Concept",
                                    14: "[14]\n(W)Call offers/Call inc-end\n(W)Validate-start, (A)Validating",
                                    15: "[15]\n(W)Call inc-end, (W)Validate-start\n(A)Validating, (A)Pending\n"
                                        "(A)Offer, (W)Validate-end",
                                    16: "[16]\n(A)Create, (A)Concept\n(A)Accept, (O)Create",
                                    17: "[17]\n(W)Handle Lds-end, (A)Concept\n(A)Accept, (O)Create\n"
                                        "(W)Call offers-start, (A)Complete",
                                    18: "[18]\n(A)Accept, (O)Create",
                                    19: "[19]\n(O)Create, (W)Complete appl-end\n(W)Call offers-start, (A)Complete"}

node_properties["operators"] = {
    "Clean bench prep-authorize product_start": ["triangle", "0.3", "0.3", "#aec7e8"],
    "Clean bench prep-authorize product_complete": ["triangle", "0.3", "0.3", "#1f77b4"],
    "Clean bench prep-format string_start": ["triangle", "0.3", "0.3", "#ffff99"],
    "Clean bench prep-format string_complete": ["triangle", "0.3", "0.3", "#dec718"],
    "Clean bench prep-label from printer 1_start": ["triangle", "0.3", "0.3", "#98df8a"],
    "Clean bench prep-label from printer 1_complete": ["triangle", "0.3", "0.3", "#2ca02c"],
    "Clean bench prep-send task list_start": ["triangle", "0.3", "0.3", "#ff9896"],
    "Clean bench prep-send task list_complete": ["triangle", "0.3", "0.3", "#d62728"],
    "Clean bench prep-wait for product present_start": ["triangle", "0.3", "0.3", "#c5b0d5"],
    "Clean bench prep-wait for product present_complete": ["triangle", "0.3", "0.3", "#9467bd"],
    "Clean bench prep-wait for stage finished_start": ["triangle", "0.3", "0.3", "#c49c94"],
    "Clean bench prep-wait for stage finished_complete": ["triangle", "0.3", "0.3", "#8c564b"],
    "Cleanbench-authorize product_start": ["invtriangle", "0.3", "0.3", "#aec7e8"],
    "Cleanbench-authorize product_complete": ["invtriangle", "0.3", "0.3", "#1f77b4"],
    "Cleanbench-send task list_start": ["invtriangle", "0.3", "0.3", "#ff9896"],
    "Cleanbench-send task list_complete": ["invtriangle", "0.3", "0.3", "#d62728"],
    "Cleanbench-wait for component scan_start": ["invtriangle", "0.3", "0.3", "#f7b6d2"],
    "Cleanbench-wait for component scan_complete": ["invtriangle", "0.3", "0.3", "#e377c2"],
    "Cleanbench-wait for scan_start": ["invtriangle", "0.3", "0.3", "#c7c7c7"],
    "Cleanbench-wait for scan_complete": ["invtriangle", "0.3", "0.3", "#7f7f7f"],
    "Cleanbench-wait for stage finished_start": ["invtriangle", "0.3", "0.3", "#c49c94"],
    "Cleanbench-wait for stage finished_complete": ["invtriangle", "0.3", "0.3", "#8c564b"],
    "Final Checker-authorize product_start": ["square", "0.3", "0.3", "#aec7e8"],
    "Final Checker-authorize product_complete": ["square", "0.3", "0.3", "#1f77b4"],
    "Final Checker-global tester": ["square", "0.3", "0.3", "#ffffff"],
    "Final Checker-send dut recipe_start": ["square", "0.3", "0.3", "#9edae5"],
    "Final Checker-send dut recipe_complete": ["square", "0.3", "0.3", "#17becf"],
    "Final Checker-wait for product present_start": ["square", "0.3", "0.3", "#c5b0d5"],
    "Final Checker-wait for product present_complete": ["square", "0.3", "0.3", "#9467bd"],
    "Final Checker-wait for stage finished_start": ["square", "0.3", "0.3", "#c49c94"],
    "Final Checker-wait for stage finished_complete": ["square", "0.3", "0.3", "#8c564b"],
    "Inner Assembly-authorize product_start": ["star", "0.3", "0.3", "#aec7e8"],
    "Inner Assembly-authorize product_complete": ["star", "0.3", "0.3", "#1f77b4"],
    "Inner Assembly-send task list_start": ["star", "0.3", "0.3", "#ff9896"],
    "Inner Assembly-send task list_complete": ["star", "0.3", "0.3", "#d62728"],
    "Inner Assembly-wait for component scan_start": ["star", "0.3", "0.3", "#f7b6d2"],
    "Inner Assembly-wait for component scan_complete": ["star", "0.3", "0.3", "#e377c2"],
    "Inner Assembly-wait for stage finished_start": ["star", "0.3", "0.3", "#c49c94"],
    "Inner Assembly-wait for stage finished_complete": ["star", "0.3", "0.3", "#8c564b"],
    "Inner Assembly-wait for scan_start": ["star", "0.3", "0.3", "#c7c7c7"],
    "Inner Assembly-wait for scan_complete": ["star", "0.3", "0.3", "#7f7f7f"],
    "Open Frame Checker-authorize product_start": ["circle", "0.3", "0.3", "#aec7e8"],
    "Open Frame Checker-authorize product_complete": ["circle", "0.3", "0.3", "#1f77b4"],
    "Open Frame Checker-global tester": ["circle", "0.3", "0.3", "#ffffff"],
    "Open Frame Checker-send dut recipe_start": ["circle", "0.3", "0.3", "#9edae5"],
    "Open Frame Checker-send dut recipe_complete": ["circle", "0.3", "0.3", "#17becf"],
    "Open Frame Checker-wait for product present_start": ["circle", "0.3", "0.3", "#c5b0d5"],
    "Open Frame Checker-wait for product present_complete": ["circle", "0.3", "0.3", "#9467bd"],
    "Open Frame Checker-wait for stage finished_start": ["circle", "0.3", "0.3", "#c49c94"],
    "Open Frame Checker-wait for stage finished_complete": ["circle", "0.3", "0.3", "#8c564b"],
    "Outer Assembly-authorize product_start": ["diamond", "0.3", "0.3", "#aec7e8"],
    "Outer Assembly-authorize product_complete": ["diamond", "0.3", "0.3", "#1f77b4"],
    "Outer Assembly-label from printer 1_start": ["diamond", "0.3", "0.3", "#98df8a"],
    "Outer Assembly-label from printer 1_complete": ["diamond", "0.3", "0.3", "#2ca02c"],
    "Outer Assembly-send task list_start": ["diamond", "0.3", "0.3", "#ff9896"],
    "Outer Assembly-send task list_complete": ["diamond", "0.3", "0.3", "#d62728"],
    "Outer Assembly-wait for scan_start": ["diamond", "0.3", "0.3", "#c7c7c7"],
    "Outer Assembly-wait for scan_complete": ["diamond", "0.3", "0.3", "#7f7f7f"],
    "Outer Assembly-wait for stage finished_start": ["diamond", "0.3", "0.3", "#c49c94"],
    "Outer Assembly-wait for stage finished_complete": ["diamond", "0.3", "0.3", "#8c564b"],
    "Packing-authorize product_start": ["rect", "0.15", "0.3", "#aec7e8"],
    "Packing-authorize product_complete": ["rect", "0.15", "0.3", "#1f77b4"],
    "Packing-label for printer 1_start": ["rect", "0.15", "0.3", "#86b4a9"],
    "Packing-label for printer 1_complete": ["rect", "0.15", "0.3", "#39737c"],
    "Packing-label for printer 2_start": ["rect", "0.15", "0.3", "#dbdb8d"],
    "Packing-label for printer 2_complete": ["rect", "0.15", "0.3", "#bcbd22"],
    "Packing-send task list_start": ["rect", "0.15", "0.3", "#ff9896"],
    "Packing-send task list_complete": ["rect", "0.15", "0.3", "#d62728"],
    "Packing-wait for scan_start": ["rect", "0.15", "0.3", "#c7c7c7"],
    "Packing-wait for scan_complete": ["rect", "0.15", "0.3", "#7f7f7f"],
    "Packing-wait for stage finished_start": ["rect", "0.15", "0.3", "#c49c94"],
    "Packing-wait for stage finished_complete": ["rect", "0.15", "0.3", "#8c564b"],
}

abbr_dict["operators"] = {
    "Clean bench prep-authorize product_start": ["triangle", "0.3", "0.3", "#aec7e8"],
    "Clean bench prep-authorize product_complete": ["triangle", "0.3", "0.3", "#1f77b4"],
    "Clean bench prep-format string_start": ["triangle", "0.3", "0.3", "#ffff99"],
    "Clean bench prep-format string_complete": ["triangle", "0.3", "0.3", "#dec718"],
    "Clean bench prep-label from printer 1_start": ["triangle", "0.3", "0.3", "#98df8a"],
    "Clean bench prep-label from printer 1_complete": ["triangle", "0.3", "0.3", "#2ca02c"],
    "Clean bench prep-send task list_start": ["triangle", "0.3", "0.3", "#ff9896"],
    "Clean bench prep-send task list_complete": ["triangle", "0.3", "0.3", "#d62728"],
    "Clean bench prep-wait for product present_start": ["triangle", "0.3", "0.3", "#c5b0d5"],
    "Clean bench prep-wait for product present_complete": ["triangle", "0.3", "0.3", "#9467bd"],
    "Clean bench prep-wait for stage finished_start": ["triangle", "0.3", "0.3", "#c49c94"],
    "Clean bench prep-wait for stage finished_complete": ["triangle", "0.3", "0.3", "#8c564b"],
    "Cleanbench-authorize product_start": ["invtriangle", "0.3", "0.3", "#aec7e8"],
    "Cleanbench-authorize product_complete": ["invtriangle", "0.3", "0.3", "#1f77b4"],
    "Cleanbench-send task list_start": ["invtriangle", "0.3", "0.3", "#ff9896"],
    "Cleanbench-send task list_complete": ["invtriangle", "0.3", "0.3", "#d62728"],
    "Cleanbench-wait for component scan_start": ["invtriangle", "0.3", "0.3", "#f7b6d2"],
    "Cleanbench-wait for component scan_complete": ["invtriangle", "0.3", "0.3", "#e377c2"],
    "Cleanbench-wait for scan_start": ["invtriangle", "0.3", "0.3", "#c7c7c7"],
    "Cleanbench-wait for scan_complete": ["invtriangle", "0.3", "0.3", "#7f7f7f"],
    "Cleanbench-wait for stage finished_start": ["invtriangle", "0.3", "0.3", "#c49c94"],
    "Cleanbench-wait for stage finished_complete": ["invtriangle", "0.3", "0.3", "#8c564b"],
    "Final Checker-authorize product_start": ["square", "0.3", "0.3", "#aec7e8"],
    "Final Checker-authorize product_complete": ["square", "0.3", "0.3", "#1f77b4"],
    "Final Checker-global tester": ["square", "0.3", "0.3", "#ffffff"],
    "Final Checker-send dut recipe_start": ["square", "0.3", "0.3", "#9edae5"],
    "Final Checker-send dut recipe_complete": ["square", "0.3", "0.3", "#17becf"],
    "Final Checker-wait for product present_start": ["square", "0.3", "0.3", "#c5b0d5"],
    "Final Checker-wait for product present_complete": ["square", "0.3", "0.3", "#9467bd"],
    "Final Checker-wait for stage finished_start": ["square", "0.3", "0.3", "#c49c94"],
    "Final Checker-wait for stage finished_complete": ["square", "0.3", "0.3", "#8c564b"],
    "Inner Assembly-authorize product_start": ["star", "0.3", "0.3", "#aec7e8"],
    "Inner Assembly-authorize product_complete": ["star", "0.3", "0.3", "#1f77b4"],
    "Inner Assembly-send task list_start": ["star", "0.3", "0.3", "#ff9896"],
    "Inner Assembly-send task list_complete": ["star", "0.3", "0.3", "#d62728"],
    "Inner Assembly-wait for component scan_start": ["star", "0.3", "0.3", "#f7b6d2"],
    "Inner Assembly-wait for component scan_complete": ["star", "0.3", "0.3", "#e377c2"],
    "Inner Assembly-wait for stage finished_start": ["star", "0.3", "0.3", "#c49c94"],
    "Inner Assembly-wait for stage finished_complete": ["star", "0.3", "0.3", "#8c564b"],
    "Inner Assembly-wait for scan_start": ["star", "0.3", "0.3", "#c7c7c7"],
    "Inner Assembly-wait for scan_complete": ["star", "0.3", "0.3", "#7f7f7f"],
    "Open Frame Checker-authorize product_start": ["circle", "0.3", "0.3", "#aec7e8"],
    "Open Frame Checker-authorize product_complete": ["circle", "0.3", "0.3", "#1f77b4"],
    "Open Frame Checker-global tester": ["circle", "0.3", "0.3", "#ffffff"],
    "Open Frame Checker-send dut recipe_start": ["circle", "0.3", "0.3", "#9edae5"],
    "Open Frame Checker-send dut recipe_complete": ["circle", "0.3", "0.3", "#17becf"],
    "Open Frame Checker-wait for product present_start": ["circle", "0.3", "0.3", "#c5b0d5"],
    "Open Frame Checker-wait for product present_complete": ["circle", "0.3", "0.3", "#9467bd"],
    "Open Frame Checker-wait for stage finished_start": ["circle", "0.3", "0.3", "#c49c94"],
    "Open Frame Checker-wait for stage finished_complete": ["circle", "0.3", "0.3", "#8c564b"],
    "Outer Assembly-authorize product_start": ["diamond", "0.3", "0.3", "#aec7e8"],
    "Outer Assembly-authorize product_complete": ["diamond", "0.3", "0.3", "#1f77b4"],
    "Outer Assembly-label from printer 1_start": ["diamond", "0.3", "0.3", "#98df8a"],
    "Outer Assembly-label from printer 1_complete": ["diamond", "0.3", "0.3", "#2ca02c"],
    "Outer Assembly-send task list_start": ["diamond", "0.3", "0.3", "#ff9896"],
    "Outer Assembly-send task list_complete": ["diamond", "0.3", "0.3", "#d62728"],
    "Outer Assembly-wait for scan_start": ["diamond", "0.3", "0.3", "#c7c7c7"],
    "Outer Assembly-wait for scan_complete": ["diamond", "0.3", "0.3", "#7f7f7f"],
    "Outer Assembly-wait for stage finished_start": ["diamond", "0.3", "0.3", "#c49c94"],
    "Outer Assembly-wait for stage finished_complete": ["diamond", "0.3", "0.3", "#8c564b"],
    "Packing-authorize product_start": ["rect", "0.15", "0.3", "#aec7e8"],
    "Packing-authorize product_complete": ["rect", "0.15", "0.3", "#1f77b4"],
    "Packing-label for printer 1_start": ["rect", "0.15", "0.3", "#86b4a9"],
    "Packing-label for printer 1_complete": ["rect", "0.15", "0.3", "#39737c"],
    "Packing-label for printer 2_start": ["rect", "0.15", "0.3", "#dbdb8d"],
    "Packing-label for printer 2_complete": ["rect", "0.15", "0.3", "#bcbd22"],
    "Packing-send task list_start": ["rect", "0.15", "0.3", "#ff9896"],
    "Packing-send task list_complete": ["rect", "0.15", "0.3", "#d62728"],
    "Packing-wait for scan_start": ["rect", "0.15", "0.3", "#c7c7c7"],
    "Packing-wait for scan_complete": ["rect", "0.15", "0.3", "#7f7f7f"],
    "Packing-wait for stage finished_start": ["rect", "0.15", "0.3", "#c49c94"],
    "Packing-wait for stage finished_complete": ["rect", "0.15", "0.3", "#8c564b"],
}

cluster_descriptions["operators"] = {"start": "start",
                                     "end": "end",
                                     0: "[0]\n",
                                     1: "[1]\n",
                                     2: "[2]\n",
                                     3: "",
                                     4: "[4]\n",
                                     5: "[5]\n",
                                     6: "",
                                     7: "[7]\n",
                                     8: "[8]\n",
                                     9: "[9]\n",
                                     10: "[10]\n",
                                     11: "[11]\n",
                                     12: "[12]\n",
                                     13: "[13]\n",
                                     14: "[14]\n",
                                     15: "[15]\n",
                                     16: "[16]\n",
                                     17: "[17]\n",
                                     18: "[18]\n",
                                     19: "[19]\n"}

abbr_dict_lpm["operators"] = {
    "Clean bench prep-authorize product_start": ["triangle", "0.3", "0.3", "#aec7e8"],
    "Clean bench prep-authorize product_complete": ["triangle", "0.3", "0.3", "#1f77b4"],
    "Clean bench prep-format string_start": ["triangle", "0.3", "0.3", "#ffff99"],
    "Clean bench prep-format string_complete": ["triangle", "0.3", "0.3", "#dec718"],
    "Clean bench prep-label from printer 1_start": ["triangle", "0.3", "0.3", "#98df8a"],
    "Clean bench prep-label from printer 1_complete": ["triangle", "0.3", "0.3", "#2ca02c"],
    "Clean bench prep-send task list_start": ["triangle", "0.3", "0.3", "#ff9896"],
    "Clean bench prep-send task list_complete": ["triangle", "0.3", "0.3", "#d62728"],
    "Clean bench prep-wait for product present_start": ["triangle", "0.3", "0.3", "#c5b0d5"],
    "Clean bench prep-wait for product present_complete": ["triangle", "0.3", "0.3", "#9467bd"],
    "Clean bench prep-wait for stage finished_start": ["triangle", "0.3", "0.3", "#c49c94"],
    "Clean bench prep-wait for stage finished_complete": ["triangle", "0.3", "0.3", "#8c564b"],
    "Cleanbench-authorize product_start": ["invtriangle", "0.3", "0.3", "#aec7e8"],
    "Cleanbench-authorize product_complete": ["invtriangle", "0.3", "0.3", "#1f77b4"],
    "Cleanbench-send task list_start": ["invtriangle", "0.3", "0.3", "#ff9896"],
    "Cleanbench-send task list_complete": ["invtriangle", "0.3", "0.3", "#d62728"],
    "Cleanbench-wait for component scan_start": ["invtriangle", "0.3", "0.3", "#f7b6d2"],
    "Cleanbench-wait for component scan_complete": ["invtriangle", "0.3", "0.3", "#e377c2"],
    "Cleanbench-wait for scan_start": ["invtriangle", "0.3", "0.3", "#c7c7c7"],
    "Cleanbench-wait for scan_complete": ["invtriangle", "0.3", "0.3", "#7f7f7f"],
    "Cleanbench-wait for stage finished_start": ["invtriangle", "0.3", "0.3", "#c49c94"],
    "Cleanbench-wait for stage finished_complete": ["invtriangle", "0.3", "0.3", "#8c564b"],
    "Final Checker-authorize product_start": ["square", "0.3", "0.3", "#aec7e8"],
    "Final Checker-authorize product_complete": ["square", "0.3", "0.3", "#1f77b4"],
    "Final Checker-global tester": ["square", "0.3", "0.3", "#ffffff"],
    "Final Checker-send dut recipe_start": ["square", "0.3", "0.3", "#9edae5"],
    "Final Checker-send dut recipe_complete": ["square", "0.3", "0.3", "#17becf"],
    "Final Checker-wait for product present_start": ["square", "0.3", "0.3", "#c5b0d5"],
    "Final Checker-wait for product present_complete": ["square", "0.3", "0.3", "#9467bd"],
    "Final Checker-wait for stage finished_start": ["square", "0.3", "0.3", "#c49c94"],
    "Final Checker-wait for stage finished_complete": ["square", "0.3", "0.3", "#8c564b"],
    "Inner Assembly-authorize product_start": ["star", "0.3", "0.3", "#aec7e8"],
    "Inner Assembly-authorize product_complete": ["star", "0.3", "0.3", "#1f77b4"],
    "Inner Assembly-send task list_start": ["star", "0.3", "0.3", "#ff9896"],
    "Inner Assembly-send task list_complete": ["star", "0.3", "0.3", "#d62728"],
    "Inner Assembly-wait for component scan_start": ["star", "0.3", "0.3", "#f7b6d2"],
    "Inner Assembly-wait for component scan_complete": ["star", "0.3", "0.3", "#e377c2"],
    "Inner Assembly-wait for stage finished_start": ["star", "0.3", "0.3", "#c49c94"],
    "Inner Assembly-wait for stage finished_complete": ["star", "0.3", "0.3", "#8c564b"],
    "Inner Assembly-wait for scan_start": ["star", "0.3", "0.3", "#c7c7c7"],
    "Inner Assembly-wait for scan_complete": ["star", "0.3", "0.3", "#7f7f7f"],
    "Open Frame Checker-authorize product_start": ["circle", "0.3", "0.3", "#aec7e8"],
    "Open Frame Checker-authorize product_complete": ["circle", "0.3", "0.3", "#1f77b4"],
    "Open Frame Checker-global tester": ["circle", "0.3", "0.3", "#ffffff"],
    "Open Frame Checker-send dut recipe_start": ["circle", "0.3", "0.3", "#9edae5"],
    "Open Frame Checker-send dut recipe_complete": ["circle", "0.3", "0.3", "#17becf"],
    "Open Frame Checker-wait for product present_start": ["circle", "0.3", "0.3", "#c5b0d5"],
    "Open Frame Checker-wait for product present_complete": ["circle", "0.3", "0.3", "#9467bd"],
    "Open Frame Checker-wait for stage finished_start": ["circle", "0.3", "0.3", "#c49c94"],
    "Open Frame Checker-wait for stage finished_complete": ["circle", "0.3", "0.3", "#8c564b"],
    "Outer Assembly-authorize product_start": ["diamond", "0.3", "0.3", "#aec7e8"],
    "Outer Assembly-authorize product_complete": ["diamond", "0.3", "0.3", "#1f77b4"],
    "Outer Assembly-label from printer 1_start": ["diamond", "0.3", "0.3", "#98df8a"],
    "Outer Assembly-label from printer 1_complete": ["diamond", "0.3", "0.3", "#2ca02c"],
    "Outer Assembly-send task list_start": ["diamond", "0.3", "0.3", "#ff9896"],
    "Outer Assembly-send task list_complete": ["diamond", "0.3", "0.3", "#d62728"],
    "Outer Assembly-wait for scan_start": ["diamond", "0.3", "0.3", "#c7c7c7"],
    "Outer Assembly-wait for scan_complete": ["diamond", "0.3", "0.3", "#7f7f7f"],
    "Outer Assembly-wait for stage finished_start": ["diamond", "0.3", "0.3", "#c49c94"],
    "Outer Assembly-wait for stage finished_complete": ["diamond", "0.3", "0.3", "#8c564b"],
    "Packing-authorize product_start": ["rect", "0.15", "0.3", "#aec7e8"],
    "Packing-authorize product_complete": ["rect", "0.15", "0.3", "#1f77b4"],
    "Packing-label for printer 1_start": ["rect", "0.15", "0.3", "#86b4a9"],
    "Packing-label for printer 1_complete": ["rect", "0.15", "0.3", "#39737c"],
    "Packing-label for printer 2_start": ["rect", "0.15", "0.3", "#dbdb8d"],
    "Packing-label for printer 2_complete": ["rect", "0.15", "0.3", "#bcbd22"],
    "Packing-send task list_start": ["rect", "0.15", "0.3", "#ff9896"],
    "Packing-send task list_complete": ["rect", "0.15", "0.3", "#d62728"],
    "Packing-wait for scan_start": ["rect", "0.15", "0.3", "#c7c7c7"],
    "Packing-wait for scan_complete": ["rect", "0.15", "0.3", "#7f7f7f"],
    "Packing-wait for stage finished_start": ["rect", "0.15", "0.3", "#c49c94"],
    "Packing-wait for stage finished_complete": ["rect", "0.15", "0.3", "#8c564b"],
}
