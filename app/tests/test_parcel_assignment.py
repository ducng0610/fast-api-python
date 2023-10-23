import pytest

from app.services.parcel_assignment import AssignmentService


class TestAssignmentService:
    @pytest.mark.anyio
    async def test_assign_parcels__use_all_trains(
        self, sample_train, sample_parcel
    ):
        train1 = await sample_train(
            {
                "name": "T1",
                "cost": 10.00,
                "weight": 8.00,
                "volume": 5.00,
            }
        )
        train2 = await sample_train(
            {
                "name": "T2",
                "cost": 10.00,
                "weight": 10.00,
                "volume": 6.00,
            }
        )

        parcel1 = await sample_parcel(
            {
                "weight": 5.0,
                "volume": 2.0,
            }
        )
        parcel2 = await sample_parcel(
            {
                "weight": 2.0,
                "volume": 1.0,
            }
        )
        parcel3 = await sample_parcel(
            {
                "weight": 3.0,
                "volume": 1.0,
            }
        )
        parcel4 = await sample_parcel(
            {
                "weight": 4.0,
                "volume": 2.0,
            }
        )
        parcel5 = await sample_parcel(
            {
                "weight": 4.0,
                "volume": 3.0,
            }
        )

        svc = AssignmentService(
            parcels=[parcel1, parcel2, parcel3, parcel4, parcel5],
            trains=[train1, train2],
        )
        results, costs = svc.process()

        assert costs == 20
        assert results == {
            train1.id: [parcel5.id, parcel4.id],
            train2.id: [parcel1.id, parcel2.id, parcel3.id],
        }

    @pytest.mark.anyio
    async def test_assign_parcels__select_trains(
        self, sample_train, sample_parcel
    ):
        train1 = await sample_train(
            {
                "name": "T1",
                "cost": 10.00,
                "weight": 1.00,
                "volume": 1.00,
            }
        )
        train2 = await sample_train(
            {
                "name": "T2",
                "cost": 11.00,
                "weight": 1.00,
                "volume": 1.00,
            }
        )
        train3 = await sample_train(
            {
                "name": "T3",
                "cost": 12.00,
                "weight": 1.00,
                "volume": 1.00,
            }
        )
        train4 = await sample_train(
            {
                "name": "T4",
                "cost": 50.00,
                "weight": 5.00,
                "volume": 1.00,
            }
        )
        train5 = await sample_train(
            {
                "name": "T5",
                "cost": 130.00,
                "weight": 13.00,
                "volume": 1.00,
            }
        )
        train6 = await sample_train(
            {
                "name": "T6",
                "cost": 120.00,
                "weight": 3.00,
                "volume": 1.00,
            }
        )

        parcel1 = await sample_parcel(
            {
                "weight": 5.0,
                "volume": 1.0,
            }
        )
        parcel2 = await sample_parcel(
            {
                "weight": 2.0,
                "volume": 1.0,
            }
        )
        parcel3 = await sample_parcel(
            {
                "weight": 3.0,
                "volume": 1.0,
            }
        )
        parcel4 = await sample_parcel(
            {
                "weight": 4.0,
                "volume": 1.0,
            }
        )

        svc = AssignmentService(
            parcels=[parcel1, parcel2, parcel3, parcel4],
            trains=[train1, train2, train3, train4, train5, train6],
        )
        results, costs = svc.process()

        assert costs == 130
        assert results == {train5.id: [parcel3.id, parcel2.id, parcel1.id]}
