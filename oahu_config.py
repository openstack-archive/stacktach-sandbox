import oahu.config
from oahu import debugging
from oahu import mongodb_driver as driver
from oahu import trigger_definition
from oahu import pipeline_callback
from oahu import criteria


# We determine which operation this is by the first of these we see.
OPERATIONS = [
    'compute.instance.shutdown.start',
    'compute.instance.delete.start',
    'compute.instance.snapshot.start',
    'compute.instance.create.start',
    'compute.instance.reboot.start',
    'compute.instance.rebuild.start',
    'compute.instance.resize.start',
    'compute.instance.finish_resize.start',
    'compute.instance.resize.confirm.start',
    'compute.instance.resize.prep.start',
    'compute.instance.power_off.start',
    'compute.instance.rescue.start',
    'compute.instance.unrescue.start',
]


class RequestIdCallback(pipeline_callback.PipelineCallback):
    def on_trigger(self, stream, scratchpad):
        if not len(stream.events):
            return

        # Try to guess the operation by the first know event_type ...
        operation = None
        for e in stream.events:
            if e['event_type'] in OPERATIONS:
                operation = e['event_type']
                break
        scratchpad['operation'] = operation

        # How long did this operation take?
        first = stream.events[0]
        last = stream.events[-1]
        delta = last['timestamp'] - first['timestamp']

        scratchpad['request_id'] = first['_context_request_id']
        scratchpad['delta'] = delta

    def commit(self, stream, scratchpad):
        print "Req: %s %s time delta = %s" % (scratchpad['request_id'],
                                                 scratchpad['operation'],
                                                 scratchpad['delta'])


class EodExistsCallback(pipeline_callback.PipelineCallback):
    def on_trigger(self, stream, scratchpad):
        print "EOD-Exists:", stream
        #for event in stream.events:
        #    print event['timestamp'], event['event_type']

    def commit(self, stream, scratchpad):
        pass


class Config(oahu.config.Config):
    def get_driver(self):
        self.request_id_callback = RequestIdCallback()
        self.eod_exists_callback = EodExistsCallback()

        # Trigger names have to be consistent across all workers
        # (yagi and daemons).
        by_request = trigger_definition.TriggerDefinition("request-id",
                              ["_context_request_id", ],
                              criteria.Inactive(60),
                              [self.request_id_callback,],
                              debug=True)

        # This trigger requires a Trait called "when_date" which is
        # the date-only portion of the "when" trait. We will create
        # streams based on uuid for a given day. The distiller will
        # create this trait for us.
        instance_usage = trigger_definition.TriggerDefinition("eod-exists",
                              ["payload/instance_id", "audit_bucket"],
                              criteria.EndOfDayExists(
                                    'compute.instance.exists'),
                              [self.eod_exists_callback,],
                              debug=True,
                              dumper=debugging.DetailedDumper())

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
