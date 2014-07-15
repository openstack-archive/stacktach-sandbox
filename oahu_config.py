import oahu.config
from oahu import mongodb_sync_engine as driver
from oahu import pipeline
from oahu import stream_rules
from oahu import trigger_callback
from oahu import trigger_rule


class Callback(object):
    def on_trigger(self, stream):
        print "Processing", stream


class Config(oahu.config.Config):
    def get_sync_engine(self, callback=None):
        inactive = trigger_rule.Inactive(60)
        rule_id = "request-id"  # Has to be consistent across yagi workers.
        if not callback:
            self.callback = Callback()
        else:
            self.callback = callback
        by_request = stream_rules.StreamRule(rule_id,
                                             ["request_id", ],
                                             inactive, self.callback)
        rules = [by_request, ]

        return driver.MongoDBSyncEngine(rules)

    def get_ready_chunk_size(self):
        return 100

    def get_expiry_chunk_size(self):
        return 1000

    def get_completed_chunk_size(self):
        return -1
