import typing

from d3m import container
from d3m.metadata import base as metadata_base, hyperparams, params
from d3m.primitive_interfaces import base, transformer, unsupervised_learning
from d3m.contrib.primitives.base import installation

from d3m import __author__, __version__

__all__ = ('NullTransformerPrimitive', 'NullUnsupervisedLearnerPrimitive', 'NullDataFrameUnsupervisedLearnerPrimitive')

Inputs = container.List
Outputs = container.List


class Hyperparams(hyperparams.Hyperparams):
    pass


class Params(params.Params):
    pass


class NullTransformerPrimitive(transformer.TransformerPrimitiveBase[Inputs, Outputs, Hyperparams]):
    """
    A primitive which passes through inputs as outputs.

    It does not really care if inputs is list.
    """

    metadata: typing.ClassVar[metadata_base.PrimitiveMetadata] = metadata_base.PrimitiveMetadata({
        'id': 'cc3e3626-9bbd-47e2-aef9-482011246311',
        'version': __version__,
        'name': "Produce the same as the input",
        'keywords': ['null primitive'],
        'source': {
            'name': __author__,
            'contact': 'mailto:mitar.d3m@example.com',
            'uris': [
                'https://gitlab.com/datadrivendiscovery/d3m/-/blob/master/d3m/contrib/primitives/null.py',
                'https://gitlab.com/datadrivendiscovery/d3m.git',
            ],
        },
        'installation': installation,
        'python_path': 'd3m.primitives.operator.null.TransformerCore',
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.IDENTITY_FUNCTION,
        ],
        'primitive_family': metadata_base.PrimitiveFamily.OPERATOR,
    })

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> base.CallResult[Outputs]:
        return base.CallResult(
            value=inputs
        )


class NullUnsupervisedLearnerPrimitive(unsupervised_learning.UnsupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """
    A primitive which passes through inputs as outputs.

    It does not really care if inputs is list.
    """

    metadata: typing.ClassVar[metadata_base.PrimitiveMetadata] = metadata_base.PrimitiveMetadata({
        'id': '07c5fc32-5728-455e-a0f3-058d06c25e50',
        'version': __version__,
        'name': "Produce the same as the input",
        'keywords': ['null primitive'],
        'source': {
            'name': __author__,
            'contact': 'mailto:mitar.d3m@example.com',
            'uris': [
                'https://gitlab.com/datadrivendiscovery/d3m/-/blob/master/d3m/contrib/primitives/null.py',
                'https://gitlab.com/datadrivendiscovery/d3m.git',
            ],
        },
        'installation': installation,
        'python_path': 'd3m.primitives.operator.null.UnsupervisedLearnerCore',
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.IDENTITY_FUNCTION,
        ],
        'primitive_family': metadata_base.PrimitiveFamily.OPERATOR,
    })

    def set_training_data(self) -> None:  # type: ignore
        """
        A noop.

        Parameters
        ----------
        """

        return

    def fit(self, *, timeout: float = None, iterations: int = None) -> base.CallResult[None]:
        """
        A noop.
        """

        return base.CallResult(None)

    def get_params(self) -> Params:
        """
        A noop.
        """

        return Params()

    def set_params(self, *, params: Params) -> None:
        """
        A noop.
        """

        return

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> base.CallResult[Outputs]:
        return base.CallResult(
            value=inputs
        )


DataframeInputs = container.DataFrame
DataframeOutputs = container.DataFrame


class NullDataFrameUnsupervisedLearnerPrimitive(unsupervised_learning.UnsupervisedLearnerPrimitiveBase[DataframeInputs, DataframeOutputs, Params, Hyperparams]):
    """
    A primitive which passes through inputs as outputs.

    It does not really care if inputs is a Dataframe.
    """

    metadata: typing.ClassVar[metadata_base.PrimitiveMetadata] = metadata_base.PrimitiveMetadata({
        'id': '754c552f-8182-4b6f-af08-974f0b3540c4',
        'version': __version__,
        'name': "Produce the same as the input",
        'keywords': ['null primitive'],
        'source': {
            'name': __author__,
            'contact': 'mailto:mitar.d3m@example.com',
            'uris': [
                'https://gitlab.com/datadrivendiscovery/d3m/-/blob/master/d3m/contrib/primitives/null.py',
                'https://gitlab.com/datadrivendiscovery/d3m.git',
            ],
        },
        'installation': installation,
        'python_path': 'd3m.primitives.operator.null.DataFrameUnsupervisedLearnerCore',
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.IDENTITY_FUNCTION,
        ],
        'primitive_family': metadata_base.PrimitiveFamily.OPERATOR,
    })

    def set_training_data(self) -> None:  # type: ignore
        """
        A noop.

        Parameters
        ----------
        """

        return

    def fit(self, *, timeout: float = None, iterations: int = None) -> base.CallResult[None]:
        """
        A noop.
        """

        return base.CallResult(None)

    def get_params(self) -> Params:
        """
        A noop.
        """

        return Params()

    def set_params(self, *, params: Params) -> None:
        """
        A noop.
        """

        return

    def produce(self, *, inputs: DataframeInputs, timeout: float = None, iterations: int = None) -> base.CallResult[DataframeOutputs]:
        return base.CallResult(
            value=inputs
        )
