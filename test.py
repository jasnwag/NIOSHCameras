import dualTest

pipeline, zed, config = dualTest.initialize()
print('Starting...')
pipeline, zed = dualTest.start_recording(pipeline, zed, config, 10)
pipeline.stop()
zed.disable_recording()
zed.close()
print('Done')
