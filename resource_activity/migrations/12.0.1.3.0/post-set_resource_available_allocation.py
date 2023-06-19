# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    # set allocation_id on resource.available records that have a
    # corresponding resource.allocation record (same registration, same
    # resource and non-cancelled state). only the resource.available in
    # "selected" state are handled, as "cancelled" ones are anyway in a
    # non-usable state (their state cannot be changed), and finding the
    # corresponding resource.allocation would be tricky as there can be many
    # of them.
    cr.execute(
        """
        update resource_available as rav
        set allocation_id = ral.id
        from resource_allocation as ral
        where
            rav.registration_id = ral.activity_registration_id and
            rav.resource_id = ral.resource_id and
            rav.state = 'selected' and
            ral.state <> 'cancel'
        """
    )
    # there are still resource.available records in "selected" state that
    # don’t have an allocation_id because no corresponding resource.allocation
    # record could be found. for some of them, the corresponding record is in
    # a "cancel" state, while for others its resource has changed (the
    # registration is never changed).
    # anyway, the easiest way to have a consistent state (meaning having a
    # resource.available in "selected" state for each non-cancelled
    # resource.allocation) is to delete the remaining resource.available
    # records and re-create them from the resource.allocation records that are
    # not yet linked to a resource.available record.
    cr.execute(
        """
        delete from resource_available
        where
            allocation_id is null and
            state = 'selected'
        """
    )
    cr.execute(
        """
        insert into resource_available (
            resource_id, registration_id, allocation_id, state
        )
        select
            ral.resource_id,
            ral.activity_registration_id,
            ral.id,
            'selected'
        from resource_allocation as ral
        left join resource_available as rav on
            ral.id = rav.allocation_id
        where
            ral.activity_registration_id is not null and
            ral.state <> 'cancel' and
            rav.allocation_id is null
        order by 3
        """
    )
    # now, update the quantity_allocated field of registrations.
    cr.execute(
        """
        with resource_allocation_count as (
            select rar.id, count(0) as quantity
            from resource_activity_registration as rar
            inner join resource_allocation as ral on
                ral.activity_registration_id = rar.id
            where
                ral.state <> 'cancel'
            group by 1
            order by 1
        )
        update resource_activity_registration as rar
        set quantity_allocated = rac.quantity
        from resource_allocation_count as rac
        where rar.id = rac.id
        """
    )
