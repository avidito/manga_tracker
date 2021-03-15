import json

class BountyHandler:
    """
    [Static Class] Handler to use and manage bounty list.
    """

    @staticmethod
    def _read_bounty(path):
        """
        Validate and read bounty list from path.

        Parameters
        ----------
            path    : str. Pathname for bounty file (please insert fullpath to filename and extension).
        """
        with open(path, 'r') as f:
            bounty = json.loads(f.read())
        return bounty['groups']

    @staticmethod
    def _check(website, target=None, path='bounty.json'):
        """
        Check if group with website (and/or target) exist in bounty list.

        Parameters
        ----------
            website     : str. To be checked website from bounty groups.
            target      : str (default=None). To be checked target from website's group. Give value only if checking target existence.
            path        : str (default='bounty.json'). Pathname for bounty file (please insert fullpath to filename and extension).

        Returns
        -------
        if group (or target) exist:
            bounty_list : dict. Full list of groups from bounty list.
            group       : dict. Group with inputted website (and target).
        else:
            error_code  : int. (-1) if group doesn't exist. (-2) if target doesn't exist.
        """
        bounty_list = BountyHandler._read_bounty(path)

        # Check Group. If not found, return error
        group = None
        for bounty in bounty_list:
            if (bounty['website'] == website):
                group = bounty
                break
        if (group is None):
            return -2
        elif (target is None):
            return bounty_list, group

        # Check Target,. If not found return error
        for gt in group['targets']:
            if (gt[0] == target):
                return bounty_list, group
        return -1

    @staticmethod
    def _reconstruct(bounty, message=None, path='bounty.json'):
        """
        Reconstruct bounty list with new bounty list.

        Parameters
        ----------
            bounty  : dict. New bounty list data as bounty list blueprint.
            message : str (default=None). Message for successfull reconstruct attempt.
            path    : str (deafult='bounty.json'). Pathname for bounty file (please insert fullpath to filename and extension).

        Returns
        -------
            message : str. Message upon successfull bounty list reconstruct attempt.
        """
        with open(path, 'w') as f:
            f.write(json.dumps({'groups': bounty}))
        return msg

    @staticmethod
    def show_bounty(path='bounty.json'):
        """
        Show all targets in bounty list.

        Parameters
        ----------
            path    : str (default='bounty.json'). Pathname for bounty file (please insert fullpath to filename and extension).

        Returns
        -------
            result  : str. Extracted bounty list with better visual format.
        """
        bounty_list = BountyHandler._read_bounty(path)
        result = ''
        for bounty in bounty_list:
            result += 'Website: {}\nTargets:\n'.format(bounty['website'])
            for target in bounty['targets']:
                result += '- {}\n\t{}\n'.format(*target)
            result += '\n'
        return result

    @staticmethod
    def add_target(website, alias, link):
        """
        Add target to bounty list.

        Paramaters
        ----------
            website : str. Existing website that will be added with new target.
            alias   : str. New manga title (or alias) to be inputted.
            link    : str. New manga main page URL to be inputted.

        Returns
        -------
            message : str. Message upon successfull add target attempt.
        """
        # Find target
        result = BountyHandler._check(website)
        if (result == -2):
            return "Group with website '{}' not found!".format(website)
        else:
            bounty_list, group = result

        # Add target to group
        group['targets'].append([alias, link])

        # Reconstruct bounty file
        message = BountyHandler._reconstruct(bounty_list,
                    "Successfully add '{}' to '{}'".format(alias, website))
        return message

    @staticmethod
    def remove_target(website, alias):
        """
        Remove target from bounty list.

        Parameters
        ----------
            website : str. Existing website where the target is grouped.
            alias   : str. Existing manga title (or alias) to be removed.

        Returns
        -------
            message : str. Message upon successfull remove target attempt.
        """
        # Find target
        result = BountyHandler._check(website, alias)
        if (result == -2):
            return "Group with website '{}' not found!".format(website)
        elif (result == -1):
            return "Group with target {} not found!".format(alias)
        else:
            bounty_list, group = result

        # Remove target from group
        for target in group['targets']:
            if (target[0] == alias):
                group['targets'].remove(target)
                break

        # Reconstruct bounty file
        message = BountyHandler._reconstruct(bounty_list,
                    "Successfully remove '{}' from '{}'".format(alias, website))
        return message

    @staticmethod
    def update_target(website, alias, newalias=None, newlink=None):
        """
        Update existing target in bounty list.

        Parameters
        ----------
            website : str. Existing website where the target is grouped.
            alias   : str. Existing manga title (or alias) to be updated.
            newalias: str (default=None). New manga title (or alias) for existing manga. Give value only if changing target alias.
            newlink : str (default=None). New manga main page URL to be inputted. Give value only if changing target alias.

        Returns
        -------
        if group (or target) is not found
            message : str. Message upon failed checking existence attempt.
        else
            message : str. Message upon successfull update target attempt.
        """
        # Find target
        result = BountyHandler._check(website, alias)
        if (result == -2):
            return "Group with website '{}' not found!".format(website)
        elif (result == -1):
            return "Group with target {} not found!".format(alias)
        else:
            bounty_list, group = result

        # Get target from group
        for target in group['targets']:
            if (target[0] == alias):
                p_target = target
                break

        # Edit alias (and/or link) value
        p_target[0] = newalias if (newalias) else p_target[0]
        p_target[1] = newlink if (newlink) else p_target[1]

        # Reconstruct bounty file
        message = BountyHandler._reconstruct(bounty_list,
                    "Successfully changed '{}' from '{}'".format(alias, website))
        return message
