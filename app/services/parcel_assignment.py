"""Parcel Assignment service

This service is to compute the train with lowest cost for the parcels
"""
from typing import Any, List, Mapping, Tuple

MAX_INT = float("inf")


def compute_knapsack_table_for_min(
    weights: List[int],
    costs: List[int],
) -> List[List[int]]:
    """Build the knapsack table to find the possible items that can have total cost reach
    the minimum cost

    Parameters
    ----------
    weights: List[int]
        list of weights used for the computation
    costs: List[int]
        list of costs corresponding to the weights

    Returns
    -------
    List[List[int]]
        2-D array containing the weights with corresponding cumulative costs
    """

    max_weight = sum(weights)
    n = len(weights)

    # table to store costs by weights
    K = [
        [0 if col > 0 else MAX_INT for col in range(max_weight + 1)]
        if row > 0
        else [MAX_INT] * (max_weight + 1)
        for row in range(n + 1)
    ]

    for i in range(1, n + 1):
        for w in range(1, max_weight + 1):
            if w > weights[i - 1]:
                K[i][w] = min(
                    K[i - 1][w], K[i - 1][w - weights[i - 1]] + costs[i - 1]
                )
            else:
                K[i][w] = min(K[i - 1][w], costs[i - 1])

    return K


def compute_knapsack_table_for_max(
    weights: List[int],
    costs: List[int],
) -> List[List[int]]:
    """Build the knapsack table to find the possible items that can have total cost reach
    the maximum cost

    Parameters
    ----------
    weights: List[int]
        list of weights used for the computation
    costs: List[int]
        list of costs corresponding to the weights

    Returns
    -------
    List[List[int]]
        2-D array containing the weights with corresponding cumulative costs
    """

    max_weight = sum(weights)
    n = len(weights)

    # table to store costs by weights
    K = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, max_weight + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif w >= weights[i - 1]:
                K[i][w] = max(
                    K[i - 1][w], K[i - 1][w - weights[i - 1]] + costs[i - 1]
                )
            else:
                K[i][w] = K[i - 1][w]

    return K


class AssignmentService:
    """Assignment service that will assign the parcel to approriate train"""

    def __init__(self, trains: List[object], parcels: List[object]) -> None:
        self.available_trains = trains
        self.parcels = parcels

        self.trains_data = {
            "ids": [],
            "weights": [],
            "volumes": [],
            "costs": [],
        }

        for train in trains:
            self.trains_data["ids"].append(train.id)
            self.trains_data["weights"].append(train.weight)
            self.trains_data["volumes"].append(train.volume)
            self.trains_data["costs"].append(train.cost)

        self.parcels_data = {
            "ids": [],
            "weights": [],
            "volumes": [],
        }

        for parcel in parcels:
            self.parcels_data["ids"].append(parcel.id)
            self.parcels_data["weights"].append(parcel.weight)
            self.parcels_data["volumes"].append(parcel.volume)

        self.total_parcel_weight = sum(self.parcels_data["weights"])
        self.total_parcel_volume = sum(self.parcels_data["volumes"])

    def _select_trains(self) -> List[object]:
        """Find the trains that can handle the required weight and volume
        with possible lowest minimum costs

        Returns
        -------
        List[object]
            list of selected trains
        """
        W = self.total_parcel_weight
        V = self.total_parcel_volume

        # if total weights of all trains is less than or equal total weight of packages,
        # utilize all the available trains
        if sum(self.trains_data["weights"]) <= W:
            return self.available_trains

        # costs by weights table
        Kw = compute_knapsack_table_for_min(
            weights=self.trains_data["weights"],
            costs=self.trains_data["costs"],
        )

        n = len(self.available_trains)
        min_cost = total_volumes = 0
        w = W

        checked_costs = set()

        while total_volumes < V:
            total_volumes = 0
            min_cost = cost = Kw[n][w]
            train_indexes = []

            if cost in checked_costs:
                w += 1
                continue

            for i in range(n, 0, -1):
                if cost <= 0:
                    break

                if cost == Kw[i - 1][w]:
                    continue
                else:
                    # This item is included.
                    train_indexes.append(i - 1)
                    total_volumes += self.trains_data["volumes"][i - 1]

                    # Since this weight is included
                    # its value is deducted
                    cost -= self.trains_data["costs"][i - 1]
                    w -= self.trains_data["weights"][i - 1]

            w = W + 1
            checked_costs.add(min_cost)

        return [self.available_trains[i] for i in train_indexes]

    def _assign_parcels(self, parcels: List[object], train: Any) -> List[int]:
        """Assign a list of parcels to the specific train

        Parameters
        ----------
        parcels : List[object]
            list of parcels
        train: object
            assigned train that the parcels are filled int

        Returns
        -------
        List[int]
            list of the parcel ids that are filled into the train
        """
        parcels_data = {
            "ids": [],
            "weights": [],
            "volumes": [],
        }

        for parcel in parcels:
            parcels_data["ids"].append(parcel.id)
            parcels_data["weights"].append(parcel.weight)
            parcels_data["volumes"].append(parcel.volume)
        # if total weight less than or equal train capacity
        # and total volume less than or equal train's volume, assign all
        if (
            sum(parcels_data["weights"]) <= train.weight
            and sum(parcels_data["volumes"]) <= train.volume
        ):
            return parcels_data["ids"]

        # costs by weights table
        Kw = compute_knapsack_table_for_max(
            weights=parcels_data["weights"],
            costs=parcels_data["volumes"],
        )

        n = len(parcels)
        w = train.weight
        min_volume = Kw[n][w]

        parcel_indexes = []
        for i in range(n, 0, -1):
            if min_volume <= 0:
                break

            if min_volume == Kw[i - 1][w]:
                continue
            else:
                # This item is included.
                parcel_indexes.append(i - 1)

                # Since this weight is included
                # its value is deducted
                min_volume -= parcels_data["volumes"][i - 1]
                w -= parcels_data["weights"][i - 1]

        return [parcels_data["ids"][i] for i in parcel_indexes]

    def process(self) -> Tuple[Mapping[int, List[int]], float]:
        """Start the assignment process."""

        selected_trains = []

        # if there is only 1 train available, book it anyway
        if len(self.available_trains) == 1:
            selected_trains = self.available_trains
        else:
            # select approriate trains
            selected_trains = self._select_trains()

        unassigned_ids = set(self.parcels_data["ids"])
        unassigned_parcels = self.parcels
        i = 0

        assigned_by_train = {}

        while i < len(selected_trains) and unassigned_ids:
            train = selected_trains[i]
            assigned_parcel_ids = self._assign_parcels(
                unassigned_parcels, train
            )
            assigned_by_train[train.id] = assigned_parcel_ids
            unassigned_ids = unassigned_ids - set(assigned_parcel_ids)
            unassigned_parcels = [
                p for p in self.parcels if p.id in unassigned_ids
            ]
            i += 1

        # cleaning the train that does not have any parcels
        assigned_by_train = {
            train_id: parcel_ids
            for (train_id, parcel_ids) in assigned_by_train.items()
            if parcel_ids
        }
        assigned_train = [
            train
            for train in self.available_trains
            if train.id in assigned_by_train
        ]

        total_costs = sum([t.cost for t in assigned_train])

        return assigned_by_train, total_costs
