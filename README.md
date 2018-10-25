# Readme

## Goal

This branch tackles schema matching at the *instance*
level, i.e. it looks at data stored inside two different
keys and determines if they are potentially referring to
the same thing.

## Approach

Initially, I thought classification was the way to go
and tried to use logistic regression to classify each key depending on features from the data.

A drawback which quickly became obvious is that good features
must be engineered/learned, and the incorrect results aren't very explainable/debuggable. As new types of data come
up, developers might have to go back and start implementing
custom features. Ideally, this would be avoided.

The approach adopted instead was a generative model which
reduces to Naive Bayes as applied in document classification.
Instead of looking at word chunks, positional character distributions are learned and the likelihood can be used to
pick the most likely class.

I think this approach is appealing for a few reasons:

* Character distributions for most common types of things
stored in databases, including ids, hashes, names, addresses
timestamps, descriptions, coordinate info, phone numbers, 
email, etc. are easily differentiated from their 
distributions.

* Methods to improve matching such as identifying minor changes in formatting such as ```user@email.com``` vs ```user AT email DOT com``` can build upon the learned character distributions.

* When a new data type comes along, it is a matter of learning its characterization and none of the existing classes get disturbed.

* As the model is relatively straightforward, it should prove
easier to verify that it is "doing the right thing".

The problem reduced to creating good generalizations
or models for the various classes which might come up.
To do this, I think a combination of two solutions can
be adopted:

* Have the extremely common types handled in an 
"off-the-shelf" manner, where developers just have to
specify that this class might potentially be useful
for the schema.

* Enable them to train custom models for their unique
data which doesn't fit under the above category.

To characterize these learned representations, a
transformative pipeline chaining decorators has been
 built. The model is built using an exploratory search
starting from a randomly chosen "decent" configuration.

## Tasks
- [ ] Integrate entity schema for a single period
    - [x] Perform one-one matching
    - [x] Perform matching based on word shapes
    - [ ] Use word similarity metrics to get potential matches