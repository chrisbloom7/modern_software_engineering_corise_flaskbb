# CoRise TODO: implement a class for managing topics with in a forum
class TopicManager(object):
    def __init__(self) -> None:
        pass

    def lock(topics):
        return TopicManager.modify_boolean_attribute(topics, "locked", True)

    def unlock(topics):
        return TopicManager.modify_boolean_attribute(topics, "locked", False)

    def highlight(topics):
        return TopicManager.modify_boolean_attribute(topics, "important", True)

    def trivialize(topics):
        return TopicManager.modify_boolean_attribute(topics, "important", False)

    def delete(topics):
        modified_topics = 0

        for topic in topics:
            modified_topics += 1
            topic.delete()

        return modified_topics

    def hide(topics, user):
        modified_topics = 0

        for topic in topics:
            if topic.hidden:
                continue

            modified_topics += 1
            topic.hide(user)

        return modified_topics

    def unhide(topics):
        modified_topics = 0

        for topic in topics:
            if not topic.hidden:
                continue

            modified_topics += 1
            topic.unhide()

        return modified_topics

    def modify_boolean_attribute(topics, attribute, value):
        modified_topics = 0

        for topic in topics:
            if getattr(topic, attribute) is value:
                continue

            setattr(topic, attribute, value)
            modified_topics += 1
            topic.save()

        return modified_topics
