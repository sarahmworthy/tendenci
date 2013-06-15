position_field = 'position'; // Name of inline model field (integer) used for ordering. Defaults to "position".

jQuery(function($) {    
    // Hide "position"-field (both td:s and th:s)
    var table = $("table#formset")
    table.find('td.field-' + position_field).hide();
    td_pos_field_index = table.find('tbody tr td').index(table.find('td.field-' + position_field));
    table.find('th:eq(' + (td_pos_field_index) + ')').hide();

    table.sortable({
        items: 'tr:has(td)',
        tolerance: 'pointer',
        axis: 'y',
        cancel: 'input,button,select,a',
        helper: 'clone',
        update: function() {
            update_positions(table);
        }
    });
});

// Updates "position"-field values based on row order in table
function update_positions(table, update_ids)
{
    even = true
    num_rows = 0
    position = 0;

    // Set correct position: Filter through all trs, excluding first th tr and last hidden template tr
    table.find('tbody tr').each(function() {
        if (position_field != '')
        {
            // Update position field
            $(this).find('td.field-' + position_field + ' input[type="text"]').val(position + 1);
            position++;
            
            // Update row coloring
            $(this).removeClass('row1 row2');
            if (even)
            {
                $(this).addClass('row1');
                even = false;
            }
            else
            {
                $(this).addClass('row2');
                even = true;
            }
        }
    });
    
}
