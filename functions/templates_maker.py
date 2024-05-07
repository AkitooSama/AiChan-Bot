class ProfileTemplate:
    def __init__(
        self,
        member_name=None,
        server_name=None,
        friends=None,
        best_friends=None,
        pronouns=None,
        message_count=None,
        behavior_percentage=None,
        member_details=None,
        extra_information=None,
    ):
        self.member_name = member_name if member_name is not None else 'unknown'
        self.server_name = server_name if server_name is not None else 'unknown'
        self.friends = friends if friends is not None else 'unknown'
        self.best_friends = best_friends if best_friends is not None else 'unknown'
        self.pronouns = pronouns if pronouns is not None else 'unknown'
        self.message_count = message_count if message_count is not None else 'unknown'
        self.behavior_percentage = behavior_percentage if behavior_percentage is not None else 'unknown'
        self.member_details = member_details if member_details is not None else 'unknown'
        self.extra_information = extra_information if extra_information is not None else 'unknown'

    def member_profile_template(self):
        template = f"""
        Member name is {self.member_name}.
        Member belongs to {self.server_name} server.
        Member friend's name are {self.friends}.
        Member best friend's are {self.best_friends}.
        Member pronouns are {self.pronouns}.
        Member have sent {self.message_count} messages.
        Member behavior types percentage's are {self.behavior_percentage}.
        Some other details about the member are {self.member_details}.
        Some extra information: {self.extra_information} about the Member that might help you understand and construct overall profile of the Member.
        """
        return template

if __name__ == "__main__":
    pass