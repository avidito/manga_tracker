import json

class BountyHandler:
    """
    [Static Class] Handler to use and manage bounty list.
    """

    # Private Method
    @staticmethod
    def _reconstruct(path, bounty, message=None):
        """
        Reconstruct bounty list with new bounty list.

        Parameters
        ----------
            path    : str. Pathname for bounty file (with extension).
            bounty  : dict. New bounty list data as bounty list blueprint.
            message : str (default=None). Message for successfull reconstruct attempt.

        Returns
        -------
            message : str. Message upon successfull bounty list reconstruct attempt.
        """
        with open(path, 'w') as f:
            f.write(json.dumps({'groups': bounty}))
        return message

    # Public Method
    @staticmethod
    def read_bounty(path):
        """
        Validate and read bounty list from path.

        Parameters
        ----------
            path    : str. Pathname for bounty file (with extension).

        Returns
        -------
            groups  : list. All of listed groups in bounty list.
        """
        with open(path, 'r') as f:
            bounty = json.loads(f.read())
        return bounty['groups']

    @staticmethod
    def show_bounty(path):
        """
        Show all targets in bounty list.

        Parameters
        ----------
            path    : str. Pathname for bounty file (with extension).

        Returns
        -------
            result  : list. Extracted bounty list, devided by group.
        """
        bounty_list = BountyHandler.read_bounty(path)
        result = [
            [bn['website']] + [[title, link] for title, link in bn['targets']] for bn in bounty_list
        ]
        return result

    @staticmethod
    def check_target(path, website, alias=None, duplicate=False):
        """
        Get or check a group (and target) if exist in bounty list.

        Parameters
        ----------
            path        : str. Pathname for bounty file (with extension).
            website     : str. To be checked website from bounty groups.
            alias       : str (default=None). To be checked target's alias from website's group. Give value only if checking target existence.
            duplicate   : boolean (default=False). Flag to check input's duplicate.

        Returns
        -------
        if group (or target) exist:
            bounty_list : dict. Full list of groups from bounty list.
            group_id    : int. Index of group with inputted website.
            target_id   : int. Index of target with inputted alias (only if try to get a target).
        else:
            error_code  : int. (-1) if group or target doesn't exist or duplicate.
        """
        bounty_list = BountyHandler.read_bounty(path)

        # Check Group
        group_id = None
        for id, group in enumerate(bounty_list):
            if (group['website'] == website):
                group_id = id
                break
        if (group_id is None):
            return (-1, f"Group with website '{website}' was not found!")
        elif (alias is None):
            return (bounty_list, group_id)

        # Check Target
        targets = bounty_list[group_id]['targets']
        result = None
        for id, target in enumerate(targets):
            if (target[0] == alias):
                result = (bounty_list, group_id, id)
                break
        if (duplicate):
            return (bounty_list, group_id) if (result is None) else (-1, f"Target with alias '{alias}' already exist in '{website}' group's!")
        else:
            return result if (result) else (-1, f"Target with alias '{alias}' was not found in '{website}' group's!")

    @staticmethod
    def add_target(bounty_list, group_id, website, alias, link, path):
        """
        Add target to bounty list.

        Paramaters
        ----------
            bounty_list : dict. Full list of groups from bounty list.
            group_id    : int. Index of group with inputted website.
            website     : str. Website where new target will be added.
            alias       : str. New manga title (or alias) to be inputted.
            link        : str. New manga main page URL to be inputted.
            path        : str. Pathname for bounty file (with extension).

        Returns
        -------
            message : str. Message upon successfull add target attempt.
        """
        bounty_list[group_id]['targets'].append([alias, link])
        message = BountyHandler._reconstruct(path, bounty_list,
                    f"Successfully add '{alias}' to '{website}'")
        return message

    @staticmethod
    def remove_target(bounty_list, group_id, target_id, path):
        """
        Remove target from bounty list.

        Parameters
        ----------
            bounty_list : dict. Full list of groups from bounty list.
            group_id    : int. Index of existing group with manga title (or alias) to be removed.
            target_id   : int. Index of existing target in group with manga title (or alias) to be removed.
            path        : str. Pathname for bounty file (with extension).

        Returns
        -------
            message : str. Message upon successfull remove target attempt.
        """
        website = bounty_list[group_id]['website']
        alias = bounty_list[group_id]['targets'][target_id][0]
        bounty_list[group_id]['targets'].pop(target_id)
        message = BountyHandler._reconstruct(path, bounty_list,
                    f"Successfully remove '{alias}' from '{website}'")
        return message

    @staticmethod
    def update_target(bounty_list, group_id, target_id, website, newalias, newlink, path):
        """
        Update existing target in bounty list.

        Parameters
        ----------
            bounty_list : dict. Full list of groups from bounty list.
            group_id    : int. Index of existing group with manga title (or alias) to be updated.
            target_id   : int. Index of existing target in group with manga title (or alias) to be updated.
            website     : str. Website where inputted target will be updated.
            newalias    : str. New manga title (or alias) for existing manga. Give value "" only if not changing target alias.
            newlink     : str. New manga main page URL to be inputted. Give value "" only if not changing target alias.

        Returns
        -------
        if group (or target) is not found
            message : str. Message upon failed checking existence attempt.
        else
            message : str. Message upon successfull update target attempt.
        """
        target = bounty_list[group_id]['targets'][target_id]
        oldalias = target[0]
        target[0] = target[0] if (newalias == "") else newalias
        target[1] = target[1] if (newlink == "") else newlink
        message = BountyHandler._reconstruct(path, bounty_list,
                    f"Successfully changed target '{oldalias}' from '{website}'")
        return message
