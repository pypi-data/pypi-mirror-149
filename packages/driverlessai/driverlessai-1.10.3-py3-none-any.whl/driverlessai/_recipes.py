"""Recipe module of official Python client for Driverless AI."""

import re
from typing import Any
from typing import Dict
from typing import Sequence

from driverlessai import _core
from driverlessai import _utils


class Recipe(_utils.ServerObject):
    """Interact with a recipe on the Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        super().__init__(client=client)
        self._is_custom: bool = None
        self._set_name(info.name)
        self._set_raw_info(info)

    @property
    def is_custom(self) -> bool:
        """``True`` if the recipe is custom."""
        if self._is_custom is None:
            raise NotImplementedError("Custom recipe detection not available.")
        return self._is_custom

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self!s}"

    def __str__(self) -> str:
        return self.name

    def _update(self) -> None:
        pass


class ExplainerRecipe(Recipe):
    """Interact with an explainer recipe on the Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        super().__init__(client=client, info=info)
        self._default_settings = {p.name: p.val for p in info.parameters}
        self._is_custom = not info.id.startswith("h2oai")
        self._settings: Dict[str, Any] = {}

    @property
    def for_binomial(self) -> bool:
        """``True`` if explainer works for binomial models."""
        return "binomial" in self._get_raw_info().can_explain

    @property
    def for_iid(self) -> bool:
        """``True`` if explainer works for I.I.D. models."""
        return "iid" in self._get_raw_info().model_types

    @property
    def for_multiclass(self) -> bool:
        """``True`` if explainer works for multiclass models."""
        return "multiclass" in self._get_raw_info().can_explain

    @property
    def for_regression(self) -> bool:
        """``True`` if explainer works for regression models."""
        return "regression" in self._get_raw_info().can_explain

    @property
    def for_timeseries(self) -> bool:
        """``True`` if explainer works for time series models."""
        return "time_series" in self._get_raw_info().model_types

    @property
    def id(self) -> str:
        """Identifier."""
        return self._get_raw_info().id

    @property
    def settings(self) -> Dict[str, Any]:
        """Explainer settings set by user."""
        return self._settings

    def search_settings(self, search_term: str, show_description: bool = False) -> None:
        """Search explainer settings and print results. Useful when looking for
        explainer kwargs (see ``explainer.with_settings()``) to use when
        creating interpretations.

        Args:
            search_term: term to search for (case insensitive)
            show_description: include description in results
        """
        for p in self._get_raw_info().parameters:
            if search_term.lower() in f"{p.name} {p.description}".lower():
                result = f"{p.name} | default_value: {p.val}"
                if show_description:
                    result = f"{result} | {p.description}"
                print(result)

    def with_settings(self, **kwargs: Any) -> "ExplainerRecipe":
        """Changes the explainer settings from defaults. Settings reset to
        defaults everytime this is called.

        .. note::
            To search possible explainer settings for your server version,
            use ``explainer.search_settings(search_term)``.
        """
        self._settings = {}
        for k, v in kwargs.items():
            if k not in self._default_settings:
                raise ValueError(f"Setting '{k}' not recognized.")
            self._settings[k] = v
        return self


class ExplainerRecipes:
    """Interact with explainer recipes on the Driverless AI server.

    Examples::

        # Get list of names of all explainers
        [e.name for e in dai.recipes.explainers.list()]
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> Sequence["ExplainerRecipe"]:
        """Return list of explainer recipe objects.

        Examples::

            dai.recipes.explainer.list()
        """
        return _utils.ServerObjectList(
            data=[
                ExplainerRecipe(self._client, e)
                for e in self._client._backend.list_explainers(
                    experiment_types=[],
                    explanation_scopes=[],
                    dai_model_key="",
                    keywords=[],
                    explainer_filter=[],
                )
            ],
            get_method=None,
            item_class_name=ExplainerRecipe.__name__,
        )


class ModelRecipe(Recipe):
    """Interact with a model recipe on the Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        super().__init__(client=client, info=info)
        self._is_custom = info.is_custom
        self._is_unsupervised = getattr(info, "is_unsupervised", False)

    @property
    def is_unsupervised(self) -> bool:
        """``True`` if recipe doesn't require a target column."""
        return self._is_unsupervised


class ModelRecipes:
    """Interact with model recipes on the Driverless AI server.

    Examples::

        # Get list of all custom models
        [m for m in dai.recipes.models.list() if m.is_custom]

        # Get list of names of all models
        [m.name for m in dai.recipes.models.list()]
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> Sequence["ModelRecipe"]:
        """Return list of model recipe objects.

        Examples::

            dai.recipes.models.list()
        """
        return _utils.ServerObjectList(
            data=[
                ModelRecipe(self._client, m)
                for m in self._client._backend.list_model_estimators(
                    config_overrides=""
                )
            ],
            get_method=None,
            item_class_name=ModelRecipe.__name__,
        )


class RecipeJob(_utils.ServerJob):
    """Monitor creation of a custom recipe on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_custom_recipe_job(self.key))

    def result(self, silent: bool = False) -> "RecipeJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = 0) -> str:
        """Return job status string.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """
        status = self._status()
        if verbose == 1:
            return f"{status.message} {self._get_raw_info().progress:.2%}"
        if verbose == 2:
            if status == _utils.JobStatus.FAILED:
                message = " - " + self._get_raw_info().error
            else:
                message = ""  # message for recipes is partially nonsense atm
            return f"{status.message} {self._get_raw_info().progress:.2%}{message}"
        return status.message


class Recipes:
    """Create and interact with recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._explainers = ExplainerRecipes(client)
        self._models = ModelRecipes(client)
        self._scorers = ScorerRecipes(client)
        self._transformers = TransformerRecipes(client)

    @property
    def explainers(self) -> "ExplainerRecipes":
        """See explainer recipes on the Driverless AI server."""
        _utils.check_server_support(self._client, "1.9.1", "explainers")
        return self._explainers

    @property
    def models(self) -> "ModelRecipes":
        """See model recipes on the Driverless AI server."""
        return self._models

    @property
    def scorers(self) -> "ScorerRecipes":
        """See scorer recipes on the Driverless AI server."""
        return self._scorers

    @property
    def transformers(self) -> "TransformerRecipes":
        """See transformer recipes on the Driverless AI server."""
        return self._transformers

    def create(self, recipe: str) -> None:
        """Create a recipe on the Driverless AI server.

        Args:
            recipe: path to recipe or url for recipe

        Examples::

            dai.recipes.create(
                recipe='https://github.com/h2oai/driverlessai-recipes/blob/master/scorers/regression/explained_variance.py'
            )
        """
        self.create_async(recipe).result()
        return

    def create_async(self, recipe: str) -> RecipeJob:
        """Launch creation of a recipe on the Driverless AI server.

        Args:
            recipe: path to recipe or url for recipe

        Examples::

            dai.recipes.create_async(
                recipe='https://github.com/h2oai/driverlessai-recipes/blob/master/scorers/regression/explained_variance.py'
            )
        """
        if re.match("^http[s]?://", recipe):
            key = self._client._backend.create_custom_recipe_from_url(recipe)
        else:
            key = self._client._backend._perform_recipe_upload(recipe)
        return RecipeJob(self._client, key)


class ScorerRecipe(Recipe):
    """Interact with a scorer recipe on the Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        super().__init__(client=client, info=info)
        self._is_custom = info.is_custom

    @property
    def description(self) -> str:
        """Recipe description."""
        return self._get_raw_info().description

    @property
    def for_binomial(self) -> bool:
        """``True`` if scorer works for binomial models."""
        return self._get_raw_info().for_binomial

    @property
    def for_multiclass(self) -> bool:
        """``True`` if scorer works for multiclass models."""
        return self._get_raw_info().for_multiclass

    @property
    def for_regression(self) -> bool:
        """``True`` if scorer works for regression models."""
        return self._get_raw_info().for_regression


class ScorerRecipes:
    """Interact with scorer recipes on the Driverless AI server.

    Examples::

        # Retrieve a list of binomial scorers
        [s for s in dai.recipes.scorers.list() if s.for_binomial]

        # Retrieve a list of multiclass scorers
        [s for s in dai.recipes.scorers.list() if s.for_multiclass]

        # Retrieve a list of regression scorers
        [s for s in dai.recipes.scorers.list() if s.for_regression]

        # Get list of all custom scorers
        [s for s in dai.recipes.scorers.list() if s.is_custom]

        # Get list of names of all scorers
        [s.name for s in dai.recipes.scorers.list()]

        # Get list of descriptions for all scorers
        [s.description for s in dai.recipes.scorers.list()]
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> Sequence["ScorerRecipe"]:
        """Return list of scorer recipe objects.

        Examples::

            dai.recipes.scorers.list()
        """
        return _utils.ServerObjectList(
            data=[
                ScorerRecipe(self._client, s)
                for s in self._client._backend.list_scorers(config_overrides="")
            ],
            get_method=None,
            item_class_name=ScorerRecipe.__name__,
        )


class TransformerRecipe(Recipe):
    """Interact with a transformer recipe on the Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        super().__init__(client=client, info=info)
        self._is_custom = info.is_custom


class TransformerRecipes:
    """Interact with transformer recipes on the Driverless AI server.

    Examples::

        # Get list of all custom transformers
        [m for m in dai.recipes.transformers.list() if m.is_custom]

        # Get list of names of all transformers
        [m.name for m in dai.recipes.transformers.list()]
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> Sequence["TransformerRecipe"]:
        """Return list of transformer recipe objects.

        Examples::

            dai.recipes.transformers.list()
        """
        return _utils.ServerObjectList(
            data=[
                TransformerRecipe(self._client, t)
                for t in self._client._backend.list_transformers(
                    config_overrides="",
                )
            ],
            get_method=None,
            item_class_name=TransformerRecipe.__name__,
        )
