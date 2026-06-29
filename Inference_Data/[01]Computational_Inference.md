---
creation_date: "D:20041005093000"
source_file: [01]Computational_Inference.pdf
---



---

**Page 1**


This is page i
Printer: Opaque this
1
Computational Inference
Torsten Hothorn, Marcel Dettling, Peter
Bu¨hlmann
1.1 Introduction
Recent technological developments have opened new perspectives in bio-
medical research and clinical practice, and they also changed the way in
which statistics makes progress. The main challenge is to develop compu-
tational inference tools that can deal with very high dimensional datasets
containing thousands of input variables for a few dozens of experiments
only.Suchdatastructuresdoemergeforexamplefromthegeneexpression
microarray technology, and from protein mass spectroscopy analysis.
In this chapter, we focus on tumor prognosis with gene expression data.
Given efficient data analysis tools, information from biotechnology may
representapromisingsupplementtotumorpredictionbasedontraditional
clinical factors. Let us assume that we are given previous experience from
acohortofI patients,whichmathematicallyamountstoalearningsample
L={(y ,x ),(y ,x ),...,(y ,x )}.
1 1 2 2 I I
Theinputvariablex ∈RJ containsthevector-valuedgeneexpressionpro-
i
fileofJ genesfortheithpatient.Theresponsevariablecanbebinarywith
y ∈ {0,1} coding for two different populations or classes, as for example
i
differentcancersortumorsubtypes.Fornotationalconvenience,multiclass
prediction and the analysis of survival data are to be discussed later in
Sections 1.4 and 1.7
Weplantosystematicallyexploittheinformationinthelearningsample
L for defining a rule that predicts the disease evolvement (the response
variable) from the gene expression profile x. This rule can then be applied
to novel cancer patients for establishing an early and precise prognosis,
which is often crucial for a treatment with little side-effects and good
cure rates. From a mathematical viewpoint, this amounts to learning a
function g : RJ → R which can be applied in order to predict the class


---

**Page 2**


ii Hothorn, Marcel Dettling, Peter Bu¨hlmann
membership of an observation with expression profile x via some fixed
transformation f. For example, g(x|L) = log(pˆ(x)/(1 − Pˆ(x))), where
pˆ(x) = Pcr[Y = 1|X = x] and f(g) = χ(g > 0) which yields a classifi-
cation rule respecting equal misclassification costs, where χ denotes the
indicator function. In the sequel, such procedures are referred to as clas-
sifiers. Although classification is a well-known methodology in statistics,
finding solutions to problems with many input variables or genes J but
a very limited number of patients I is challenging. A promising approach
that is suitable for high-dimensional prediction problems in bioinformatics
is to use ensemble methods that aggregate many simple classifiers into a
powerful committee.
1.1.1 Ensemble Methods
In contrast to using just a single fit from a particular method, ensemble
techniques aim at improving the predictive ability of a relatively simple
statistical learning technique by constructing linear combinations thereof.
Technically, the ensemble is written as
M
X
g (·|L)= α g (·|L ),
E(M) m m m
m=1
whereL isareweightedversionofthelearningsampleLandα arereal
m m
valued weights. Here, g is a base procedure, which we term the ‘weak
m
learner’.Forexample,g (x)maybeasimpleestimatelog(pˆ(x)/(1−pˆ(x)))
m
of the log-odds ratio. The choice of the reweighted sample L , the ag-
m
gregation weights α , as well as of the weak learner are the art of this
m
business.Bagging,boostingandrandomforests aresuchimplementations,
which will be discussed below. Apparently, the final ensemble estimator
depends on the choice of the weak learner. The most prominent choice
in high-dimensional problems are recursive partitioning methods (’classi-
fication and regression trees’), as they incorporate some form of feature
selection and tend to work well when there are more input variables than
there are observations.
We refer to Breiman et al. [1] for a detailed description on recursive
partitioning methods. The rpart package [2] essentially implements the
methodology described by Breiman et al. [1].
1.2 Bagging & Random Forests
Bagging [3] is a rather simple but effective ensemble method. Its name is
an acronym for bootstrap aggegating which suggests the principle idea of
thisprocedure:PredictionsofweaklearnersfittedtobootstrapsamplesL
m
of the original learning sample L are aggregated by a majority vote.


---

**Page 3**


1. Computational Inference iii
A bootstrap sample from the original learning sample L is an i.i.d. ran-
dom sample of I observations (y∗,x∗),i = 1,...,I, where the probability
i i
of selecting observation (y∗,x∗) from L is 1/I. A bootstrap sample is thus
i i
a sample from the empirical distribution function of the learning sample.
The algorithm works as follows.
1. Draw M bootstrap samples L ,m = 1,...M, from the original
m
learning sample L.
2. Fit a weak learner for each of the bootstrap samples g (·|L ), and
m m
construct the classifiers f(g (·|L )).
m m
3. Aggregate the classifiers using weights α = 1/M, yielding the
m
ensemble
M
X
g (·|L)=M−1 f(g (·|L )).
E(M) m m
m=1
Thus, the ensemble yields the fraction of weak learners predicting class
1. The bagging ensemble votes for class 1 if the majority of the M weak
learners votes for 1; and vice versa. More generally, the ensemble predicts
class 1 when the fraction of weak learners predicting class 1 exceeds some
number ν.
Ithasbeenarguedthatforunstableestimationmethodssuchasdecision
trees, bagging reduces the variance while the bias remains approximately
the same [4].
Itisratherstraightforwardtoimplementthebaggingprocedureinhigh-
levellanguageslikeS.Thebasicingredientisatreebuildingalgorithmused
for fitting trees to bootstrap samples of the learning sample.
R> simple_bagging <- function(x, lsample, M = 100,
+ nu = 0.5) {
+ I <- nrow(lsample)
+ bsample <- rmultinom(M, I, rep(1, I)/I)
+ pred <- rep(0, nrow(x))
+ for (m in 1:M) {
+ weaktree <- rpart(y ~ ., data = lsample,
+ weights = bsample[, m], control = rpart.control(xval = 0,
+ cp = 0.01))
+ prtree <- predict(weaktree, newdata = x,
+ type = "class")
+ pred <- pred + (prtree == levels(lsample$y)[2])
+ }
+ factor(pred/M > nu, levels = levels(lsample$y))
+ }
First, M random index vectors representing M bootstrap samples are
drawn from the multinomial distribution. A classification tree is fitted to


---

**Page 4**


iv Hothorn, Marcel Dettling, Peter Bu¨hlmann
the data using weights = bsample[,m] representing the mth bootstrap
sample. Large trees without applying any form of pruning whatsoever are
grown.ThevectorpredoflengthI countingthenumberoftreespredicting
the second class is updated. Finally, the function returns a factor coding
the ensemble predictions obtained from a simple majority vote.
A simple but extremely successful modification to this algorithm is the
random forest approach [5]. The basic idea is to modify the tree grow-
ing algorithm leading to even weaker components of the ensemble. This is
achieved by choosing a small random subset of inputs available for split-
ting at each stage of the recursive partitioning algorithm building the tree.
Thus, the input variables actually used in each of the weak learners are, to
a large extent, determined at random.
1.3 Boosting
BoostinghasbeenintroducedtothemachinelearningliteraturebyFreund
and Schapire [6] and has demonstrated empirical success on a wide variety
of especially high-dimensional prediction problems. The initial notion was
thatineachboostingiteration,thecasesthatweremisclassifiedinthepre-
vious round get their weights increased, whereas the weights are decreased
forcasesthatwerecorrectlyclassified.Thus,unlikeinbaggingandrandom
forests,boththeaggregationweightsα andthereweightedlearningsam-
m
ples L depend on the previous function fits g (·|L ),...,g (·|L ).
m 1 1 m−1 m−1
However,ratherthanasasequentialdatareweightingscheme,boostingcan
morefruitfullybeseenasaforwardstagewisestrategy,workingbyiterative
optimization of an empirical risk function
I
1X
R(L,p(x),L)= L(y ,p(x )), p(x)=Pr[Y =1|X =x],
I i i
i=1
from the learning set L via constrained (imposed by the weak learner)
functional gradient descent, where L(·,·) is a statistically motivated loss
function. If we employ the binomial log-likelihood
L(y,p(x))=y·log(p(x))+(1−y)·(1−p(x)),
a continuous surrogate for the 0/1-misclassification loss and a very estab-
lishedcriterionforbinaryclassification,ithasbeenshownthattheresulting
logitboost algorithm [7] yields an approximation to half of the log-odds
ratio. That is,
M (cid:18) (cid:19)
X 1 p(x)
g (x|L)= α g (x|L )≈ log .
E(M) m m m 2 1−p(x)
m=1
Hence,logitboostisalinearexpansionintermsofofweaklearnersg (·|L )
m m
on the logit scale, constructed by stagewise optimization of the binomial


---

**Page 5**


1. Computational Inference v
log-likelihood.Estimatedconditionalclassprobabilitiesareobtainedbythe
simple transformation
1
p(x)= ,
1+exp(−2g (x))
E(M)
which can be used for class prediction, using a threshold that depends
on the misclassification costs. Logitboost has been demonstrated to be a
competitive prediction algorithm for tumor classification with microarray
data [8, 9]. The procedure works as follows.
1. Initialize p(x )≡1/2,i=1,...,I;m=1;g (·|L)≡0.
i E(0)
2. Build the pseudo-response for each observation i
w = p(x )(1−p(x ))
i i i
y −p(x )
u = i i ,
i w
i
setup-up the new learning sample
L = {(u ,x );i=1,...,I}
m i i
and fit the weak learner g (·|L ) with case weights w .
m m i
3. Update ensemble g (·|L)=g (·|L)+ 1g (·|L ) and
E(m) E(m−1) 2 m m
p(x )=1/(1+exp(−2g (x |L)))
i E(m) i
4. repeat until m=M.
Predictions are computed with α =1/2 and f(z)=χ(exp(1−2z)> 1).
m 2
The definition of the weights w in the logitboost algorithm is such that
i
each weak learner is forced to focus on observations close to the decision
boundary, i.e., data points where the boosting classifier is in doubt about
the predicted class. The final number of boosting iterations M regulates
the complexity of the prediction model, early stopping is a form of shrink-
age. In the context of microarray data, we recommend a default value of
M =100,whichisareasonablecompromisebetweencomputingtime,pre-
dictiveaccuracyandpreventionofoverfitting.Thischoicewasshowntobe
empirically superior to approaches where M was estimated on the training
dataviacrossvalidation[8].Providedthataninterfacetotheweaklearning
algorithmispresent,animplementationofboostinginhigh-levellanguages
like S is straightforward and simply consists of a loop that incorporate all
the updating operations and the weak learner fit.
1.4 Multiclass Problems
Sincethereareoftennogenesthataccuratelydiscriminatemultipleclasses,
we recommend to split K-class problems into multiple binary ones. In


---

**Page 6**


vi Hothorn, Marcel Dettling, Peter Bu¨hlmann
the context of microarray data, we have collected some empirical evi-
dence that this is more accurate than simultaneous multiclass approaches
[8]. The simplest solution is the one-against-all approach, which works
by defining the response in the kth problem as y(k) = 1 if y = k, and
y(k) =0else.Then,wearerunningboostingK timesonthemodifieddata
L(k) = {(y(k),x ),...,(y(k),x )}. The estimated conditional class proba-
1 1 I I
bilities are normalized and can in turn be used for maximum likelihood
classification via
p(k)(x) =
Pcr
L(k)
(y(k) =1|x)
b
K−1
P Pcr
L(k)
(y(k) =1|x)
k=0
y(x) = argmax p(k)(x)
b b
k∈{0,...,K−1}
.
Depending on the data, other schemes than one-against-all may be more
accurate for splitting polytomous into multiple binary problems.
Note that no additional procedures are necessary in order to deal
with multiclass responses for bagging trees or random forests: Estimated
conditional class probabilities arise directly from the ensemble of trees.
1.5 Evaluation
The choice of an appropriate classifier for a prediction problem at hand is
by no means obvious. Two problems can be separated: The method selec-
tion and the error rate estimation tasks. The first task is concerned with
choosing the best method available from a, possible huge, set of statistical
procedurescapabletodealwiththeproblem.Forthesecondone,wetryto
come up with a realistic assessment of the prediction error of the selected
procedure. This information is extremely important when we need to take
the decision whether it is worth or even ethical to apply a certain classifier
in realistic setups.
The prediction error is measured by a scalar loss function L(y,yˆ) as-
sessing the goodness of the prediction yˆ for some response y. When the
response is a categorical variable with classes {0,...,K − 1}, the mis-
classification error L(y,yˆ) = χ(y 6= yˆ) is an often used loss function.
However, this choice is not necessarily the one we are interested in. When
we are faced with a two class problem aiming at predicting whether a
person suffers a rare but dangerous disease or not the loss of missing an
affectedpersonismuchhighercomparedtothelossinducedbyafalsepos-
itive detection. For such problems, the misclassification loss is of the form
L(y,yˆ) = c χ(y = 0,yˆ= 1)+c χ(y = 1,yˆ= 0) for some misclassification
1 2
costs c ,c . We may be also interested in measuring the accuracy of the
1 2


---

**Page 7**


1. Computational Inference vii
estimated probability pˆ(x): Then, the negative log-likelihood can serve as
a useful loss function.
A major problem is that the learning sample used for model fitting can
not be used for the estimation of the prediction error of that model. Such
an estimate would be optimistically biased because the same observations
were used for model building and evaluation. Resampling methods like
the bootstrap or cross-validation have been studied extensively, a practical
introductioncanbefoundin[10].Here,wewillusethenotionofout-of-bag
estimation[11].WhenabootstrapsampleoftheoriginallearningsampleL
is drawn some observations are left out due to sampling with replacement.
Those observations can be used as independent sample for the assessment
ofthepredictionerror.Wecandrawrandomsamplesfromthedistribution
of the prediction error as follows.
1. DrawB bootstrapsamplesL ,b=1,...B,fromtheoriginallearning
b
sample L.
2. Fit a model to each bootstrap sample L , i.e. g(·|L ) and assess the
b b
error p by the loss averaged over the predictions of the observations
b
in the out-of-bootstrap sample
X
p =|L\L |−1 L(f(g(x|L ))),y), b=1,...,B.
b b b
(y,x)∈L\Lb
The B error rates can now be visualized, for example by means of box-
plots orcan be describedvia estimates ofcertain parameters such as mean
orvariance,say.Whenmultiplecandidatesmodelsareunderconsideration,
we obtain a sample of B error rates for each of them: Those distributions
canbecomparedinordertoidentifythebestorasetofthebestalgorithms.
Thenull-hypothesisofequalityofthebootstrap-distributionsofthepredic-
tion error of several algorithms can be tested, for example by means of the
Friedmantest.Itshouldbenotedthatarejectionofthishypothesisshould
notbegeneralizedtothepopulationfromwhichthedatawasdrawn,since
the inference is conditional on the given learning sample. All what we can
conclude is whether a finite number B of bootstrap replicates is sufficient
for detecting performance differences in the exact bootstrap distributions,
withB =∞(orfromthetypicallyinfeasibleexactmultinomialdistribution
inducedbythebootstrap),ofdifferentalgorithms.Theoreticaljustification
and illustration of this approach can be found elsewhere [12].
1.6 Applications: Tumor Prediction
1.6.1 Acute Lymphoblastic Leukemia
In this first example, we apply ensemble methods to construct a model
that regresses the stage of acute lymphoblastic leukemia (ALL) on the


---

**Page 8**


viii Hothorn, Marcel Dettling, Peter Bu¨hlmann
microarray expression levels. We are primarily interested in two questions.
At the one hand, we would like to investigate if there is any information
about the stage of the disease covered by the microarray expression levels,
i.e.,atestofthenull-hypothesisthatthestageofthediseaseisindependent
of the expression levels measured. If we are able to reject this global null-
hypothesis, we want to build a model that allows us to predict the stage
of the disease of a patient based on the microarray expression levels only.
DatafrompatientssufferingfrombothT-andB-cellleukemiaareavailable
from the study of Chiaretti et al. [13], and we restrict ourselves to patients
with B-cell leukemia. reference to chapter?
The package ALL offers a data object ALL, an object of class exprSet,
which contains the data of patients suffering from both T- and B-cell
leukemia.
R> pkgload <- require(Biobase, quietly = TRUE)
Welcome to Bioconductor
Vignettes contain introductory material. To view,
simply type: openVignette()
For details on reading vignettes, see
the openVignette help page.
R> pkgload <- require(ALL, quietly = TRUE)
R> data(ALL)
We are provided with expression levels of 12625 genes for 128 patients.
For the analysis here, we restrict the data to patients suffering B-cell
leukemia,with5subclasses,andtoexpressionlevelsofgeneswithcoefficient
of variation between 0.08 and 0.18.
R> cvv <- apply(exprs(ALL), 1, function(x) sd(x)/mean(x))
R> ok <- cvv > 0.08 & cvv < 0.18
R> BStagelev <- paste("B", c("", 1:4), sep = "")
R> BALL <- ALL[ok, ALL$BT %in% BStagelev]
R> pData(phenoData(BALL))$BStage <- factor(BALL$BT,
+ levels = BStagelev)
The class distribution of the stages of the disease (BALL$BStage) can be
inspected via
R> table(BALL$BStage)
B B1 B2 B3 B4
5 19 36 23 12
and is depicted by means of a barplot in Figure 1.1.
Although we selected 3841 genes showing a reasonable variation among
the patients, some mild form of univariate variable selection will help to
circumvent computational difficulties. Here, we measure the association


---

**Page 9**


1. Computational Inference ix
R> barplot(table(BALL$BStage))
B B1 B2 B3 B4
53
03
52
02
51
01
5
0
Figure 1.1. Class distribution of the stages of B-cell leukemia.
betweentheexpressionlevelsofeachgeneandthestageofthedisease,our
responsevariable,bymeansofalinearstatisticbasedontherawexpression
levels and a matrix of dummy-codings for the response. The statistics are
standardizedbytheirconditionalexpectationandvariance[14]andthe100
genes associated with the largest standardized statistics are selected.
R> response <- BALL$BStage
R> I <- ncol(exprs(BALL))
R> expressions <- exprs(BALL)
R> Iindx <- 1:I
R> ymat <- model.matrix(~response - 1)
R> var_selection <- function(indx, p = 100) {
+ y <- ymat[indx, , drop = FALSE]
+ x <- expressions[, indx, drop = FALSE]
+ n <- nrow(y)
+ linstat <- x %*% y
+ Ey <- matrix(colMeans(y), nrow = 1)
+ Vy <- matrix(rowMeans((t(y) - as.vector(Ey))^2),
+ nrow = 1)
+ rSx <- matrix(rowSums(x), ncol = 1)
+ rSx2 <- matrix(rowSums(x^2), ncol = 1)
+ E <- rSx %*% Ey
+ V <- n/(n - 1) * kronecker(Vy, rSx2)


---

**Page 10**


x Hothorn, Marcel Dettling, Peter Bu¨hlmann
+ V <- V - 1/(n - 1) * kronecker(Vy, rSx^2)
+ stats <- abs(linstat - E)/sqrt(V)
+ stats <- do.call("pmax", as.data.frame(stats))
+ return(which(stats > sort(stats)[length(stats) -
+ p]))
+ }
R> selected <- var_selection(Iindx)
The function var selection takes an index vector of observations between
1 and I and returns a vector of length p indicating which genes have been
selected.Now,weareabletofitarandomforestmodeltothedatautilizing
the package MLInterfaces which provides an unified interface to machine
learning procedures including the randomForest package [15]. Here, we use
the data of all observations except the Ith one as learning sample and
obtain information from the model on the Ith observation.
R> pkgload <- require(MLInterfaces, quietly = TRUE)
R> rf <- randomForestB(BALL[selected, ], "BStage",
+ Iindx[-1], sampsize = I - 1)
R> print(rf)
MLOutput instance, method= randomForest
Call:
randomForestB(exprObj = BALL[selected, ], classifLab = "BStage",
trainInd = Iindx[-1], sampsize = I - 1)
predicted class distribution:
B2
1
TheframeworkfortheevaluationofclassifierssketchedinSection1.5can
be implemented as follows. We loop over B bootstrap samples, perform a
variableselectionforthecurrentbootstrapsampleandfitfourmodelstothe
selectedgenesofthisbootstrapsample.First,arandomforestmodelwhere
only mtry = 3 genes are evaluated in each node of the classification trees,
bagging (which corresponds to random forest without random sampling
of genes) and logitboost with M = 100 boosting iterations. In addition,
the performance of a model that does not take any information about the
expression levels into account is investigated. To be more specific, for each
bootstrap sample we guess the class with maximal prior probability for
all observations. The misclassification errors computed for each model and
bootstrap sample are stored into a dataframe performance.
R> set.seed(290875)
R> B <- 100
R> if (!file.exists("ALLperformance.Rda")) {
+ performance <- as.data.frame(matrix(0, nrow = B,
+ ncol = 4))


---

**Page 11**


1. Computational Inference xi
+ colnames(performance) <- c("RF", "Bagg", "LBoost",
+ "Guess")
+ for (b in 1:B) {
+ bsample <- sample(Iindx, I, replace = TRUE)
+ selected <- var_selection(bsample)
+ rf3 <- randomForestB(BALL[selected, ],
+ "BStage", bsample, mtry = 3, sampsize = I)
+ predicted3 <- factor(rf3@predLabels, levels = levels(response))
+ performance[b, 1] <- mean(response[-bsample] !=
+ predicted3)
+ rfBagg <- randomForestB(BALL[selected,
+ ], "BStage", bsample, mtry = length(selected),
+ sampsize = I)
+ predictedBagg <- factor(rfBagg@predLabels,
+ levels = levels(response))
+ performance[b, 2] <- mean(response[-bsample] !=
+ predictedBagg)
+ lb <- logitboostB(BALL[selected, ], "BStage",
+ bsample, 100)
+ predictedlb <- factor(lb@predLabels, levels = levels(response))
+ performance[b, 3] <- mean(response[-bsample] !=
+ predictedlb)
+ performance[b, 4] <- mean(response[-bsample] !=
+ levels(response)[which.max(tabulate(response[bsample]))])
+ }
+ save(performance, file = "ALLperformance.Rda")
+ } else {
+ load("ALLperformance.Rda")
+ }
The distributions of the misclassification errors of all four models can be
analyzedbytheappropriateproceduresforpairedobservations.Theglobal
null-hypothesis of equality of all three models can be tested using
R> friedman.test(as.matrix(performance))
Friedman rank sum test
data: as.matrix(performance)
Friedman chi-squared = 183.6596, df = 3, p-value <
2.2e-16
which leads to a rejection indicating that there are global differences be-
tweentheperformancesofthefourcandidatemodels.Thisresultallowsus
to conclude that there is a relationship between expression levels and the
stageofB-cellleukemia.Aparallelcoordinateplotandboxplotshelpusto
investigate where the differences come from (Figure 1.2).


---

**Page 12**


xii Hothorn, Marcel Dettling, Peter Bu¨hlmann
R> layout(matrix(c(1, 2), ncol = 2))
R> matplot(1:ncol(performance), t(performance), type = "l",
+ col = 1, lty = 1, xlab = "", ylab = "Misclassification error",
+ axes = FALSE)
R> axis(1, at = 1:ncol(performance), labels = colnames(performance))
R> axis(2)
R> box()
R> boxplot(performance)
rorre
noitacifissalcsiM
RF Bagg LBoost Guess
8.0
7.0
6.0
5.0
4.0
3.0
l
l
l
l
l
l
RF Bagg LBoost Guess
8.0
7.0
6.0
5.0
4.0
3.0
Figure1.2.Parallelcoordinatesplotandboxplotsofthemisclassificationerrorsof
random forest (RF), bagging (Bagg), logitboost (LBoost) and guessing (Guess)
for 100 bootstrap samples for the ALL data.
Thefiguresleadtotheimpressionthatthethreeensemblemethodsperform
betterthanguessingwithoutusinginformationaboutgeneexpressionpro-
files.Randomforestandbaggingseemtoperformequallygood,theamount
of the difference can be inspected by confidence intervals, for example via
R> t.test(performance$RF, performance$Bagg, paired = TRUE,
+ conf.int = TRUE)
Paired t-test
data: performance$RF and performance$Bagg
t = -0.4623, df = 99, p-value = 0.6449
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
-0.01627441 0.01012377


---

**Page 13**


1. Computational Inference xiii
sample estimates:
mean of the differences
-0.00307532
We emphasize again, see end of Section 1.5, that the Friedman test and
thegraphicalillustrationsindicatewhethertherearedifferencesamongthe
theoretical bootstrap distributions (with B = ∞), although we compute
with B =100 only.
1.6.2 Renal Cell Cancer
In this second application, we focus on the relationship between gene ex-
pression levels and response variables describing either clinical subtypes of
renal cell cancer or, most interesting in a clinical setting, the survival time
of the patients. The package kidpack offers data of a study by Su¨ltmann et
al. [16] explained in detail in Chapter XXX . The analysis is very similar Chapter ref?
to the steps described for the ALL data in Section 1.6.1.
First, we load the package kidpack which offers the raw data in form of
an exprSet.
R> set.seed(290875)
R> pkgload <- require(kidpack, quietly = TRUE)
R> data(eset)
R> pData(phenoData(eset))$type <- as.factor(eset$type)
The class distribution of clear cell renal cancer ccRCC, papillary renal cell
cancerpRCCandchromophoberenalcellcancerchRCCisdepictedinFigure
1.3.Again,astandardizedlinearstatisticforeachgeneisappliedtoperform
variable selection:
R> response <- eset$type
R> expressions <- exprs(eset)
R> I <- ncol(exprs(eset))
R> Iindx <- 1:I
R> ymat <- model.matrix(~response - 1)
R> var_selection <- function(indx, p = 100) {
+ y <- ymat[indx, , drop = FALSE]
+ x <- expressions[, indx, drop = FALSE]
+ n <- nrow(y)
+ linstat <- x %*% y
+ Ey <- matrix(colMeans(y), nrow = 1)
+ Vy <- matrix(rowMeans((t(y) - as.vector(Ey))^2),
+ nrow = 1)
+ rSx <- matrix(rowSums(x), ncol = 1)
+ rSx2 <- matrix(rowSums(x^2), ncol = 1)
+ E <- rSx %*% Ey
+ V <- n/(n - 1) * kronecker(Vy, rSx2)


---

**Page 14**


xiv Hothorn, Marcel Dettling, Peter Bu¨hlmann
R> barplot(table(pData(phenoData(eset))$type))
ccRCC chRCC pRCC
05
04
03
02
01
0
Figure 1.3. Class distribution of the renal cell cancer data
+ V <- V - 1/(n - 1) * kronecker(Vy, rSx^2)
+ stats <- abs(linstat - E)/sqrt(V)
+ stats <- do.call("pmax", as.data.frame(stats))
+ return(which(stats > sort(stats)[length(stats) -
+ p]))
+ }
R> selected <- var_selection(Iindx)
andarandomforestmodelfortheIthpatientcanbefittedto100selected
genes using
R> rf <- randomForestB(eset[selected, ], "type",
+ Iindx[-1], sampsize = I - 1)
R> rf
MLOutput instance, method= randomForest
Call:
randomForestB(exprObj = eset[selected, ], classifLab = "type",
trainInd = Iindx[-1], sampsize = I - 1)
predicted class distribution:
ccRCC
1


---

**Page 15**


1. Computational Inference xv
Themisclassificationerrorforthefourmodels(randomforest,bagging,log-
itboostandguessing)appliedtobootstrapsamplesofthedataiscomputed
along the following lines:
R> B <- 100
R> if (!file.exists("kidpackperformance.Rda")) {
+ performance <- as.data.frame(matrix(0, nrow = B,
+ ncol = 4))
+ colnames(performance) <- c("RF", "Bagg", "LBoost",
+ "Guess")
+ for (b in 1:B) {
+ bsample <- sample(Iindx, I, replace = TRUE)
+ selected <- var_selection(bsample)
+ rf3 <- randomForestB(eset[selected, ],
+ "type", bsample, mtry = 3, sampsize = I)
+ predicted3 <- factor(rf3@predLabels, levels = levels(response))
+ performance[b, 1] <- mean(response[-bsample] !=
+ predicted3)
+ rfBagg <- randomForestB(eset[selected,
+ ], "type", bsample, mtry = length(selected),
+ sampsize = I)
+ predictedBagg <- factor(rfBagg@predLabels,
+ levels = levels(response))
+ performance[b, 2] <- mean(response[-bsample] !=
+ predictedBagg)
+ lb <- logitboostB(eset[selected, ], "type",
+ bsample, 100)
+ predictedlb <- factor(lb@predLabels, levels = levels(response))
+ performance[b, 3] <- mean(response[-bsample] !=
+ predictedlb)
+ performance[b, 4] <- mean(response[-bsample] !=
+ levels(response)[which.max(tabulate(response[bsample]))])
+ }
+ save(performance, file = "kidpackperformance.Rda")
+ } else {
+ load("kidpackperformance.Rda")
+ }
Again, the global null-hypothesis of equality of the performance of the
candidate models can be rejected
R> friedman.test(as.matrix(performance))
Friedman rank sum test
data: as.matrix(performance)


---

**Page 16**


xvi Hothorn, Marcel Dettling, Peter Bu¨hlmann
rorre
noitacifissalcsiM
RF Bagg LBoost Guess
5.0
4.0
3.0
2.0
1.0
0.0
l
l ll
l
l
RF Bagg LBoost Guess
5.0
4.0
3.0
2.0
1.0
0.0
Figure1.4.Parallelcoordinatesplotandboxplotsofthemisclassificationerrorsof
random forest (RF), bagging (Bagg), logitboost (LBoost) and guessing (Guess)
for 100 bootstrap samples for the renal cell cancer data.
Friedman chi-squared = 217.7669, df = 3, p-value <
2.2e-16
which, in the light of Figure 1.4, can be explained by the superior perfor-
manceoftheensemblemethodscomparedtothemodelwhereweguessthe
prediction from the prior distribution of the classes itself. Random forests
seem to perform a little bit better compared to bagging and show a per-
formance similar to logitboost, as the confidence interval for the difference
indicate:
R> t.test(performance$RF, performance$Bagg, paired = TRUE,
+ conf.int = TRUE)
Paired t-test
data: performance$RF and performance$Bagg
t = -5.3201, df = 99, p-value = 6.455e-07
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
-0.03182856 -0.01453612
sample estimates:
mean of the differences
-0.02318234


---

**Page 17**


1. Computational Inference xvii
R> t.test(performance$RF, performance$LBoost, paired = TRUE,
+ conf.int = TRUE)
Paired t-test
data: performance$RF and performance$LBoost
t = -0.7676, df = 99, p-value = 0.4445
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
-0.012479551 0.005517086
sample estimates:
mean of the differences
-0.003481233
The same comment as at the end of Section 1.6.1 applies here as well.
1.7 Applications: Survival Analysis
Mainly in clinical studies, the disease free survival time or overall survival
time is of major interest. For each observation, we are provided with the
time for which each patient was under risk and whether a target event
(recurrence, death) occurred or if the observation was stopped for other
reasons(forexamplealethalaccident).Moreformally,theresponsevariable
isnowbivariatewithy ∈R+×{0,1}.Weareinterestedinanassessmentof
i
the survival time to be expected for a patient with expression levels x, i.e.,
an assessment of the conditional probability that this patient will survive
time t given the patients gene expression levels.
Basically,theingredientsofthebaggingalgorithmforthetwo-classprob-
lem can be applied to those problems as well. However, it is a challenge to
aggregate the predictions of the multiple trees in order to come up with a
ensembleprediction.Asimpleaverageofthepredictedsurvivaltimedidnot
provetobeofmuchuse[17].Asanalternative,Hothornetal.[18]suggested
to aggregate observations instead of predictions directly and compute one
single prediction based on aggregated observations. For each of the M sur-
vival trees fitted to bootstrap samples L ,m = 1,...,M, we extract the
m
observationsfromthebootstrapsamplewhichareelementofthesameter-
minal node the predictor value x of interest. Those observations, of course
containing many tied values, are collected over all M bootstrap rounds,
and then one single Kaplan-Meier curve is computed which serves as the
ensemble’s prediction.
R> pkgload <- require(survival, quietly = TRUE)
R> pkgload <- require(ipred, quietly = TRUE)
R> pkgload <- require(exactRankTests, quietly = TRUE)
R> remove <- is.na(pData(phenoData(eset))$survival.time)


---

**Page 18**


xviii Hothorn, Marcel Dettling, Peter Bu¨hlmann
R> seset <- eset[, !remove]
R> response <- Surv(seset$survival.time, seset$died)
R> response[response[, 1] == 0] <- 1
R> expressions <- exprs(seset)
R> exprDF <- as.data.frame(t(expressions))
R> I <- nrow(exprDF)
R> Iindx <- 1:I
The survival time of patients with renal cell cancer is now treated as the
response variable of interest. First, we remove all observations where the
survival time is missing (14 observations) from the data set and redefine
zero survival times (one observation).
The response variable is now an object of class Surv. A slightly differ-
ent test statistic needs to be used for the variable selection. Here, we use
logrank scores as implemented in the cscores method from package exac-
tRankTests andtheexpressionvaluesforeachgeneandapplyateststatistic
measuring the correlation between each gene and the logrank scores which
is standardized by the conditional expectation and variance. Because of
the small number of patients with information on the survival time being
available, we only select 25 genes at a time.
R> var_selection <- function(indx, p = 25) {
+ y <- matrix(cscores(response[indx]), ncol = 1)
+ x <- expressions[, indx, drop = FALSE]
+ n <- nrow(y)
+ linstat <- x %*% y
+ Ey <- matrix(colMeans(y), nrow = 1)
+ Vy <- matrix(rowMeans((t(y) - as.vector(Ey))^2),
+ nrow = 1)
+ rSx <- matrix(rowSums(x), ncol = 1)
+ rSx2 <- matrix(rowSums(x^2), ncol = 1)
+ E <- rSx %*% Ey
+ V <- n/(n - 1) * kronecker(Vy, rSx2)
+ V <- V - 1/(n - 1) * kronecker(Vy, rSx^2)
+ stats <- abs(linstat - E)/sqrt(V)
+ stats <- do.call("pmax", as.data.frame(stats))
+ return(which(stats > sort(stats)[length(stats) -
+ p]))
+ }
R> selected <- var_selection(Iindx)
Theensembleofsurvialtreesisfittedtothedatausingthebagging method
(package ipred [19]). The predictions for each observation in the learning
sample are computed based on trees whose corresponding bootstrap sam-
ples did not contain the specific observation (out-of-bootstrap prediction)
andarethereforenotaffectedbyoverfittingproblems.Inaddition,wecom-


---

**Page 19**


1. Computational Inference xix
pute a simple Kaplan-Meier curve for the survival times via survfit. The
‘model fit’ of both procedures may be assessed by means of the Brier score
for censored data [20] implemented in the function sbrier.
R> bagg <- bagging(response ~ ., data = exprDF[,
+ selected], ntrees = 100)
R> prKM <- predict(bagg)
R> sbrier(response, prKM)
integrated Brier score
0.1284143
attr(,"time")
[1] 1 65
R> sbrier(response, survfit(response))
integrated Brier score
0.2069643
attr(,"time")
[1] 1 65
Thisresultseemstoindicatethatthesurvivalensemblefitsthedatabetter
than a model without knowledge of the gene expression data and hence
that there is information about the survival time covered by the expres-
sion levels. The predicted survival curves for each patient and the simple
Kaplan-MeierestimateofallsurvivaltimesaredepictedinFigure1.5show-
ingareasonaledifferentiationbetweenthepatients.Ifthisfindingisreliable
needs to be addressed by a benchmark comparison with a model that pre-
dicts the survival time without knowledge of the gene expression values,
i.e., a simple Kaplan-Meier estimate.
R> set.seed(290875)
R> B <- 100
R> if (!file.exists("Survperformance.Rda")) {
+ performance <- as.data.frame(matrix(0, nrow = B,
+ ncol = 2))
+ colnames(performance) <- c("Bagging", "Kaplan-Meier")
+ for (b in 1:B) {
+ bsample <- sample(Iindx, I, replace = TRUE)
+ selected <- var_selection(bsample)
+ bagg <- bagging(response ~ ., data = exprDF[,
+ selected], subset = bsample, ntrees = 100)
+ pr <- predict(bagg, newdata = exprDF[-bsample,
+ ])
+ KM <- survfit(response[bsample])
+ performance[b, 1] <- sbrier(response[-bsample],
+ pr)
+ performance[b, 2] <- sbrier(response[-bsample],


---

**Page 20**


xx Hothorn, Marcel Dettling, Peter Bu¨hlmann
R> plot(survfit(response), lwd = 4, conf.int = FALSE,
+ xlab = "Survival time in month", ylab = "Probability")
R> KMlines <- lapply(prKM, lines, lty = 2)
0 10 20 30 40 50 60
0.1
8.0
6.0
4.0
2.0
0.0
Survival time in month
ytilibaborP
Figure 1.5. Out-of-bootstrap predicted survival curves for each patient (dashed
lines) and overall Kaplan-Meier curve (thick solid line).
+ KM)
+ }
+ save(performance, file = "Survperformance.Rda")
+ } else {
+ load("Survperformance.Rda")
+ }
The visualizations of the Brier scores in Figure 1.6 indicate differences
with respect to the variability but not with respect to the mean Brier
score and hence we cannot conclude that the survival time of a patient
can adequately modeled based on information derived from gene expres-
sion profiling. Note that this benchmark experiment is based on a learning
sampleof60patients,42ofwhicharecensored.Thisimpliesthat,onaver-
age,only38uniquepatientsareincludedinonebootstraplearningsample,
which explains the large variability.
The same comment as at the end of Section 1.6.1 applies here as well.


---

**Page 21**


1. Computational Inference xxi
serocs
reirB
Bagging Kaplan−Meier
53.0
03.0
52.0
02.0
51.0
01.0
l
Bagging Kaplan−Meier
53.0
03.0
52.0
02.0
51.0
01.0
Figure 1.6. Parallel coordinates plot and boxplots of the Brier scores of 100
bootstrap samples for renal cell cancer survival.
1.8 Conclusions
Modeling the relationship between a clinically interesting response vari-
able, such as tumor subtype of survival time, and gene expression levels of
thousands of genes for only a small number of patients is a challenge to
statistical methodology. The analyses in this chapter give an overview on
ensemblemethodsformodelinghigh-dimensionalgeneexpressiondataand
illustratebothadvantagesandshortcomings.Fortypicalsamplesizesinthe
orderof100patients,ensemblemethodsseemappropriateforconstructing
models for the prediction of tumor subtypes of renal cell cancer or stages
of B-cell leukemia. It should be noted though that ensemble methods as
used here are not more than black-box prediction methods. Modeling cen-
sored time-to-event data in such a high-dimensional setting is even more
difficult,especiallywhenasubstantialnumberofpatientsarecensored.Fi-
nally, we would like to mention that much research is currently conducted
in the field of ensemble methods in both statistics and machine learning
andonecanexpectfurthermethodologicaldevelopmentsandnewsoftware
packages offering more functionality in the near future.


---

**Page 22**


xxii Hothorn, Marcel Dettling, Peter Bu¨hlmann
References
[1] Breiman,L.,Friedman,J.H.,Olshen,R.A.,andStone,C.J.:Classification
and regression trees.California, Wadsworth, 1984.
[2] Therneau,T.M.andAtkinson,E.J.Anintroductiontorecursivepartition-
ing using the rpart routine.Technical Report 61, Section of Biostatistics,
Mayo Clinic, Rochester, 1997.
[3] Breiman, L.: Bagging predictors.Machine Learning.24(2): 123–140, 1996.
[4] Bu¨hlmann,P.andYu,B.:Analyzingbagging.TheAnnalsofStatistics.30(4):
927–961, 2002.
[5] Breiman, L.: Random forests.Machine Learning.45(1): 5–32, 2001.
[6] Freund, Y. and Schapire, R. E.: Experiments with a new boosting
algorithm.In Saitta, L. (Ed.): Machine Learning: Proceedings of the Thir-
teenthInternationalConference.SanFrancisco,MorganKaufmann,1996,pp
148–156.
[7] Friedman, J., Hastie, T., and Tibshirani, R.: Additive logistic regression:
A statistical view of boosting.The Annals of Statistics.28(2): 337–407,
2000.with Discussion.
[8] Dettling,M.andBu¨hlmann,P.:Boostingfortumorclassificationwithgene
expression data.Bioinformatics.19(9): 1061–1069, 2003.
[9] Dettling, M. and Bu¨hlmann, P.: Finding predictive gene groups from
microarray data.Journal of Multivariate Analysis.90(1): 106–131, 2004.
[10] Hastie,T.,Tibshirani,R.,andFriedman,J.H.:TheElementsofStatistical
Learning : Data Mining, Inference, and Prediction.Springer Verlag, 2001.
[11] Breiman, L.Out-of-bag estimation.Technical report, Statistics Department,
University of California Berkeley, Berkeley CA 94708, 1996.
[12] Hothorn, T., Leisch, F., Zeileis, A., and Hornik, K.The design and analysis
ofbenchmarkexperiments.TechnicalReport82,SFBAdaptiveInformations
Systems and Management in Economics and Management Science, 2004.
[13] Chiaretti, S., Li, X., Gentleman, R., Vitale, A., Vignetti, M., Mandelli, F.,
Ritz, J., and Foa, R.: Gene expression profile of adult T-cell acute lympho-
cytic leukemia identifies distinct subsets of patients with different response
to therapy and survival.Blood.103(7): 2771–2778, 2004.
[14] Strasser, H. and Weber, C.: On the asymptotic theory of permutation
statistics.Mathematical Methods of Statistics.8: 220–250, 1999.
[15] Liaw, A. and Wiener, M.: Classification and regression by randomForest.R
News.2(3): 18–22, December 2002.
[16] Su¨ltmann, H., von Heydebreck, A., Huber, W., Kuner, R., Buneß, A.,
Vogt, M., Gunawan, B., Vingron, M., Fu¨zes´ı, L., and Poustka, A.:
Gene expression in kidney cancer is associated with novel tumor sub-
types, cytogenetic abnormalities and metastasis formation.Clinical Cancer
Research.2004.accepted.
[17] Dannegger, F.: Tree stability diagnostics and some remedies for instabil-
ity.Statistics in Medicine.19(4): 475–491, 2000.


---

**Page 23**


1. Computational Inference xxiii
[18] Hothorn, T., Lausen, B., Benner, A., and Radespiel-Tr¨oger, M.: Bagging
survival trees.Statistics in Medicine.23(1): 77–91, 2004.
[19] Peters, A., Hothorn, T., and Lausen, B.: ipred: Improved predictors.R
News.2(2): 33–36, June 2002.ISSN 1609-3631.
[20] Graf,E.,Schmoor,C.,Sauerbrei,W.,andSchumacher,M.:Assessmentand
comparison of prognostic classification schemes for survival data.Statistics
in Medicine.18(17-18): 2529–2545, November 1999.
