import json

class BountyHandler:
    """
    Module to Use and Manage Bounty List.
    """

    @staticmethod
    def _read_bounty(path):
        """
        Validate and read bounty list.
        """
        with open(path, 'r') as f:
            bounty = json.loads(f.read())
        return bounty['groups']

    @staticmethod
    def _check(website, target=None, path='bounty.json'):
        """
        Check if group of website (and/or target) exist.
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
    def _reconstruct(bounty, msg=None, path='bounty.json'):
        """
        Reconstruct bounty list.
        """
        with open(path, 'w') as f:
            f.write(json.dumps({'groups': bounty}))
        return msg

    @staticmethod
    def show_bounty(path='bounty.json'):
        """
        Show all targets in bounty list.
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
