try:
    import syft as sy
    from .exec.remote_compute import RemoteCompute
    from .exec.execute_compute import ExecuteRemoteComputeMQTT
except:
    print("Loading Distributed Embeddings libraries only, skipping federated deep learning.")
    pass
from .exec.embeddings import ParseAndExecute as EmbeddingParseAndExecute, AlgorithmsApplier, BeginWorker
