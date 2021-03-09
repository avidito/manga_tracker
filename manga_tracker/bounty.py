import json

from .database import DatabaseEngine
from .log import Logger

class BountyHandler:
    """
    Module to Use and Manage Bounty List.
    """
    def __init__(self, path):
        self.path = path
        self.bounty = self._read_bounty()

    def _read_bounty(self):
        """
        Validate and read bounty list.
        """
        with open(self.path, 'r') as f:
            bounty = json.loads(f.read())
        return bounty['bounty']

    def _check(self, website, target=None):
        """
        Check if group of website (and/or target) exist.
        """
        # Check Group
        group = None
        for bounty in self.bounty:
            if (bounty['website'] == website):
                group = bounty
                break

        # If group is not exist, return error
        if (group is None):
            return -2
        elif (target is None):
            return group

        # If checking target, check target in group
        for gt in group['targets']:
            if (gt[0] == target):
                return group

        # If not found target, return error
        return -1

    def _reconstruct(self, msg=None):
        """
        Reconstruct bounty list.
        """
        with open(self.path, 'w') as f:
            f.write(json.dumps({'bounty': self.bounty}))
        print(msg)

    def show_bounty(self):
        """
        Show all target in bounty list.
        """
        for bounty in self.bounty:
            print("Website: {}\nTargets:".format(bounty['website']))
            for target in bounty['targets']:
                print("- {}\n\t{}".format(*target))
            print('')

    def add_target(self, website, alias, link):
        """
        Add target to bounty list.
        """
        # Find target
        group = self._check(website)
        if (group == -2):
            return "Group with website {} not found!".format(website)

        # Add target to group
        group['targets'].append([alias, link])

        # Reconstruct bounty file
        self._reconstruct("Successfully add '{}' to '{}'".format(alias, website))

    def remove_target(self, website, alias):
        """
        Remove target from bounty list.
        """
        # Find target
        group = self._check(website, alias)
        if (group == -2):
            return "Group with website {} not found!".format(website)
        elif (group == -1):
            return "Group with target {} not found!".format(alias)

        # Remove target from group
        for target in group['targets']:
            if (target[0] == alias):
                group['targets'].remove(target)
                break

        # Reconstruct bounty file
        self._reconstruct("Successfully remove '{}' from '{}'".format(alias, website))

    def update_target(self, website, alias, new_alias=None, new_link=None):
        """
        Update existing target in bounty list.
        """
        # Find target
        group = self._check(website, alias)
        if (group == -2):
            return "Group with website {} not found!".format(website)
        elif (group == -1):
            return "Group with target {} not found!".format(alias)

        # Get target from group
        for target in group['targets']:
            if (target[0] == alias):
                p_target = target
                break

        # Edit alias (and/or link) value
        p_target[0] = new_alias if (new_alias) else p_target[0]
        p_target[1] = new_link if (new_link) else p_target[1]

        # Reconstruct bounty file
        self._reconstruct("Successfully changed '{}' from '{}'".format(alias, website))
