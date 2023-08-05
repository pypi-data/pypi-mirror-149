***********
Overview
***********


This library implements a set of algorithms to create **compact models**: smaller versions of models with accuracy
similar to their original version. The strategy is to use a much more powerful model to guide the training of
a small model.

Here's a typical use-case:

* You are interested in building a Decision Tree with ``depth <=5``. We informally refer to this as the *small model*.
* First, you create a powerful *oracle* model. Say, Gradient Boosted Decision Trees.
* Then, you use this to train the Decision Tree. The benefit is the small model is likely to have greater accuracy than if you had trained it normally, i.e., without the oracle.

When might you want this?

* **Interpretability**: if you want a model to be interpretable by humans, it typically implies it cannot be large. This library allows you to create compact versions of your preferred model family/library. This was our motivation.
* **Compressed Models**: you might want small models because of constraints on your execution environment, like an edge device.

An important difference with some other approaches is that here you **BYOM** - *bring your own model*. We don't
prescribe a specific kind of Decision Tree, or a Linear Model, etc. You can pair up *any* oracle with *any* model.
In other words, the algorithms are **model-agnostic**. Sure, the *library* supports certain
models, but this is for convenience; you can just as well write your own models and oracles, and have the library
use them (see :any:`custom_models`).


For ex, any small model in the following table can be paired with any oracle.

.. csv-table:: Examples of small models and oracles
   :file: docs/pairings_example.csv
   :header-rows: 1


Did you notice RF and GBDT figures in both columns? Yes, you can use a larger model as an oracle to train a small model
of the *same model family*!

This seems to work on a variety of datasets across different model combinations;
check out the :any:`what_to_expect` section.

There are really just only two rules:

* The oracle must have a accuracy higher than the small model you want to train.
* The oracle must be *probabilistic*, i.e., it must produce probabilities for its label predictions.

.. tip::

   Even if you have a preferred model training algorithm for creating interpretable or small models,
   you can run it through our library *anyway* to see if you can obtain an *even* smaller model with similar accuracy.


Please :any:`cite_us` if you use the software. The software is distributed under the *Apache V2.0* :any:`LICENSE-2.0`.