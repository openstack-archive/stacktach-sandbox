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
        if not callback:
            self.callback = Callback()
        else:
            self.callback = callback

        # Trigger names have to be consistent across all workers
        # (yagi and daemons).
        by_request = trigger_definition.TriggerDefinition("request-id",
                                                      ["_context_request_id", ],
                                                      criteria.Inactive(60),
                                                      self.callback)

        # This trigger requires a Trait called "when_date" which is
        # the date-only portion of the "when" trait. We will create
        # streams based on uuid for a given day. The distiller will
        # create this trait for us.
        instance_usage = trigger_definition.TriggerDefinition("instance_id",
                              ["payload/instance_id", "audit_bucket"],
                              criteria.EndOfDayExists(
                                    'compute.instance.exists'),
                              self.callback)

        triggers = [by_request, instance_usage]

        return driver.MongoDBDriver(triggers)

    def get_distiller_config(self):
        return ""

    def get_ready_chunk_size(self):
        return 100

    def get_expiry_chunk_size(self):
        return 1000

    def get_completed_chunk_size(self):
        return -1
