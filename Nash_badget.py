import cvxpy


def print_details(utilities, subjects, subs, number_of_people, donations, preferences):
    utility_values = [u.value for u in utilities]
    BUDGET = "BUDGET: "
    for ind, s in enumerate(subjects):
        BUDGET = BUDGET + s + "=" + str(subs[ind].value)
        if ind != (len(subjects)-1):
            BUDGET += ", "

    print(BUDGET)

    for i in range(number_of_people):
        txt = "Citizen "+str(i)+" should donate  "
        for sub in preferences[i]:
            v = subs[subjects.index(sub)].value
            txt = txt + str(v*donations[i]/utilities[i].value) + " to " + sub
            if i != (number_of_people - 1):
                txt += " and "
        print(txt)


def Nash_budget(total: float, subjects: list[str], preferences: list[list[str]]):
    number_of_people = len(preferences)
    number_of_subjects = len(subjects)

    allocations = cvxpy.Variable(number_of_subjects)
    subs = allocations

    donations = [total/number_of_people]*number_of_people

    utilities = [None]*number_of_people
    for i in range(number_of_people):
        for pref in preferences[i]:
            if utilities[i] is None:
                utilities[i] = subs[subjects.index(pref)]
            else:
                utilities[i] += subs[subjects.index(pref)]

    sum_of_logs = cvxpy.sum([cvxpy.log(u) for u in utilities])
    positivity_constraints = [v >= 0 for v in allocations]
    sum_constraint = [cvxpy.sum(allocations) == sum(donations)]

    problem = cvxpy.Problem(
        cvxpy.Maximize(sum_of_logs),
        constraints=positivity_constraints+sum_constraint)
    problem.solve()

    print_details(utilities, subjects, subs, number_of_people, donations, preferences)


if __name__ == '__main__':
    subjects = ["a", "b", "c", "d"]
    total = 500
    preferences = [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['a']]

    Nash_budget(total, subjects, preferences)

