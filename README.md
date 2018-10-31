# Readme

Please skip to implementation if you just want to understand what has been
implemented in the codebase so far &ndash; section between provides
some reasoning for what has been done.

## Goal

This branch tackles schema matching at the **instance
level**, i.e. it looks at data stored inside two different
keys and determines if they are potentially storing
the same thing.

## Approach

From my understanding, this problem can be approached from
a couple of different directions.

## Classification
 Given a pair of keys (and all the
 different values linked with them for that time period),
 decide if they are sufficiently related to be classified
 as holding the same kind of data.

 **Thoughts**
   * The notion of "relation" has to be flexible.
   An useful merged schema is subjective and depends on the
   requirements of the project.

   * One-vs-rest type classifiers can be general purpose
   and be reused across projects, eg. identifying keys holding UNIX timestamps or
   a "Firstname Lastname" field might be useful for several projects,
   and training for this classifier doesn't require project specific
   information.

## Clustering (not done)
Another approach might employ the notion
 of embeddings from NLP. Data inside each key can be used
 to learn an embedding in which semantically similar keys would
 be close together.  However, training such a model will 
 be very complicated compared to the one adopted. The main advantage
 would be that the user stories could be used for matching, but
 I think this is unreliable currently and would require more data.

 **Thoughts**
   * The embedding learned would likely be through a stochastic
   process and this might not be desirable from a SWE perspective.

   * Embeddings would likely have to be relearned for each project
   and cannot be reused. Maybe some transfer learning can be done but
   there are no guarantees.

## Other challenges
*  The system must be able to adapt to information from other modules,
such as the schema level matcher or project specifications. This might
simplify the job of this module. Ideally, information flow would be both
ways so a mistake made by the schema level matcher can be notified from
the instance level, e.g. if distributions are very different

* There is a chicken-egg problem where there is almost no data at the time
such a schema matching would be done

## Implementation

To train any machine learning system requires some amount of useful
data. To try to solve this problem, I wrote a class which would
be able to "bootstrap" each classifier by providing some useful 
examples of what the actual data might look like.

For example, if the field is a phone number, it should mostly adhere
to some variation of ```abc xyz pqrs```, for example ```(123)-456-7890,
or 123-456-7890, or 1234567890```. I have implemented a way to describe
the "shape" of data by combining decorators/generators to transform a 
basic random input stream.

The main idea here is basically Naive Bayes text classification, where
learned positional character distributions for each type of key can be
used to differentiate between them.

* Character distributions for most common types of things
stored in databases, including IDs, hashes, names, addresses,
timestamps, descriptions, coordinate info, phone numbers, 
email, etc. are easily differentiated from their 
distributions.

* Methods to improve matching such as identifying minor changes in formatting such as ```user@email.com``` vs ```user AT email DOT com``` can build upon the learned character distributions.

* When a new data type comes along, it is a matter of learning its characterization and none of the existing classes get disturbed.

* As the model is relatively straightforward, it should prove
easier to verify that it is "doing the right thing".

Training these models for trivial data types will prove cumbersome,
so I think the functionality should be implemented in a framework.

* Have the extremely common types handled in an 
"off-the-shelf" manner, where developers just have to
specify that this class might potentially be useful
for the schema and keys fitting (best) this specification
are classified as such.

* Enable them to create custom models for their special
data which doesn't fit under the above category, by describing
the shape. Expose the classes required for them to do this.

There might be a case where the input 

## Tasks
- [ ] Integrate entity schema for a single period
    - [x] Perform one-one matching
    - [x] Perform matching based on word shapes
    - [ ] Use word similarity metrics to get potential matches
