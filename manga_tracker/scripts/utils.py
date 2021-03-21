from terminaltables import AsciiTable

def cvt_group_to_table(group):
    """
    Convert group information from dict format to AsciiTable.
    """
    header = ['Title', 'Link']
    tbl_website = AsciiTable([['Website: ' + group[0]]])
    tbl_targets = AsciiTable([header] + group[1:])
    return tbl_website, tbl_targets

def cvt_target_to_table(target, new=False):
    """
    Convert target information from dict format to AsciiTable.
    """
    keys = ['website', 'newalias', 'newlink'] if (new) else ['website', 'alias', 'link']
    columns = ["Website", "Alias", "URL"]
    values = [target[key] for key in keys]
    preview = [[col, val] for col, val in zip(columns, values)]
    preview_tbl = AsciiTable([['Key', 'Value']] + preview)
    return preview_tbl

def cvt_header_to_table(header):
    """
    Convert header string to AsciiTable.
    """
    return AsciiTable([[header]])

def cvt_idx_to_target(bounty_list, group_id, target_id):
    """
    Convert group id and target id into target dict.
    """
    target = {
        'website': bounty_list[group_id]['website'],
        'alias': bounty_list[group_id]['targets'][target_id][0],
        'link': bounty_list[group_id]['targets'][target_id][1]
    }
    return target
