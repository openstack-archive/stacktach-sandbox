import oahu.config
from oahu import mongodb_driver as driver
from oahu import trigger_definition
from oahu import pipeline_callback
from oahu import criteria


class Callback(pipeline_callback.PipelineCallback):
    def on_trigger(self, stream):
        print "Processing", stream


class Config(oahu.config.Config):
    def get_driver(self, callback=None):
        inactive = criteria.Inactive(60)
        trigger_name = "request-id"  # Has to be consistent across yagi workers.
        if not callback:
            self.callback = Callback()
        else:
            self.callback = callback
        by_request = trigger_definition.TriggerDefinition(trigger_name,
                                                          ["request_id", ],
                                                          inactive,
                                                          self.callback)
        triggers = [by_request, ]

        return driver.MongoDBDriver(triggers)

    def get_ready_chunk_size(self):
        return 100

    def get_expiry_chunk_size(self):
        return 1000

    def get_completed_chunk_size(self):
        return -1
