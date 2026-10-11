# From Prediction to Algorithmic Management
## AI Forecasting, Adaptive Learning, Human Decisions, and Governance

**Grand Research Institute | Research Journey**  
**Research lead:** David Grand  
**Initial working protocol:** October 11, 2026  
**Status:** Exploratory study and prospective protocol; no validated performance findings

### Abstract
This research stream examines whether AI forecasting systems improve decision quality through verified feedback, model updates, retrieval, calibration, and governance, and whether human adoption of AI recommendations changes managerial outcomes. Sports forecasts supply an accessible, timestamped decision domain, **not a gambling performance claim**. The central subject is algorithmic management: how advice, authority, learning processes, and accountability interact.

### Core research questions
1. Do feedback enabled forecasting systems outperform an unchanged model when evaluated prospectively on comparable events?
2. Does any improvement persist after controlling for outcome variance, changes in input data, and selection bias?
3. How well do stated probabilities represent observed event frequencies?
4. How often do humans accept, override, or ignore AI recommendations, and how does that behavior affect decision quality?
5. Which managerial controls provide better accountability, including authorization, versioning, audit trails, exception review, and rollback?

### Important conceptual distinction: what does learning mean?
- **Training or fine tuning:** updates model weights from selected data and feedback. Improvement is possible but not guaranteed.
- **Inference time reasoning and tools:** may improve an answer without changing persistent model weights.
- **Retrieval or external memory:** may update the information available for later decisions without retraining the base LLM.
- **Adaptive forecasting layer:** a separately managed statistical or machine learning system can update its parameters based on verified outcomes.
- **Hardware capacity:** new chips support larger models and more inference or training computation but do not, by themselves, prove greater predictive validity.
- **Chat interaction:** recording an outcome in a conversation does **not** establish that the underlying foundation model learned from it.

### Initial evidence inventory
The October 11, 2026 working discussion and associated research framework describe **four historical forecast statements** as candidates for the evidence register. The full underlying prediction records, contemporaneous timestamps, model specifications, calibrated probabilities, and externally verified outcomes have **not yet been assembled into an auditable dataset**. One specific contemporary example is the user's acceptance of an AI recommendation for the San Francisco 49ers; acceptance is an observation, **not a demonstrated successful prediction**. The relevant game outcome and pregame information should be independently checked before analysis.

Do not calculate a win rate, treatment effect, statistical significance, or an improvement trend from this preliminary inventory.

### Prospective experimental design
**Unit of analysis:** one forecast recorded before an event, linked to a defined event ID, information cutoff, and independent verified outcome.

**Arms:**
1. Frozen model baseline, using a fixed version and standardized prompt.
2. Updated forecasting workflow with auditable retrieval and feedback.
3. Human only estimate where available.
4. Human plus AI estimate, with acceptance or override logged.

Use the same event set and information cutoff across arms, preserve all forecasts including unfavorable cases, and preregister primary outcomes and exclusions before analyzing the prospective sample. Hold out future events from tuning; use temporal validation to reduce leakage.

**Minimum record fields:** unique event identifier; event date and market/context; forecast creation timestamp and time zone; model/provider/version; prompt and input provenance; data cutoff; forecast class and probability; uncertainty statement; human decision; reason for override; event outcome and verification source; evaluation timestamp; revision history; confidentiality classification.

**Primary evaluation:** Brier score for binary forecasts, log loss, calibration plots and calibration error, alongside simple reference forecasts. Report prediction coverage, missing data, and uncertainty intervals. Accuracy is secondary and should not replace probability scoring. Evaluate improvement as a difference against the frozen baseline on paired events, with uncertainty estimates and sensitivity checks.

**Human factors:** recommendation uptake, overrides, decision consistency, automation bias, and differences between advice quality and human reliance. An accepted recommendation is not proof of trustworthiness or causal influence.

**Governance:** designate responsibility for input verification, model changes, approvals, independent outcomes, incident management, and documentation; restrict retroactive alteration of predictions; maintain a clear distinction between human authorization and algorithmic execution.

### Proposed visuals (research graphics, not betting charts)
| Figure | Display | Interpretation / guardrail |
| --- | --- | --- |
| Evidence completeness | Bar chart showing records with timestamp, probability, model ID, human action, and verified outcome | Counts must derive from actual records; missing fields visibly identified |
| Forecast calibration | Reliability diagram: average predicted probability versus observed frequency | Requires sufficient independent observations and uncertainty bands |
| Forecast performance | Paired plot of baseline versus adaptive workflow Brier score across rolling evaluation windows | Lower Brier is better; indicate sample sizes and intervals |
| Human oversight | Stacked bars for accepted, overridden, and ignored advice across model versions or decision contexts | Descriptive unless a controlled study supports causal inference |
| Model learning | Longitudinal time series of prespecified scoring metric and version or feedback changes | Label updates and changes in event mix; never imply observed learning from hypothetical curves |
| Governance process | Decision flow from model forecast to human approval to independent outcome verification to approved model update | Diagram illustrates process, not measured benefit |

**Visualization ethics:** examples with invented numbers must be labeled *hypothetical illustration*. Do not use stake amounts, returns, betting odds graphics, or win/loss imagery as primary scientific figures.

### Testable propositions
- **H1:** A governed, outcome informed forecasting workflow will achieve lower prospective Brier scores than a frozen baseline, conditional on comparable events and sound validation.
- **H2:** Human reliance will increase with reported AI confidence, even when confidence is poorly calibrated; the magnitude is an empirical question.
- **H3:** Verified outcomes combined with documented management review will yield more auditable changes than unlogged feedback or retrospective narrative.
- **H4:** Increasing computational resources alone will not reliably improve decision performance absent suitable data, objective functions, and evaluation.

These are hypotheses, not established results.

### Relation to GRI Research Journey
This prospective decision laboratory complements ongoing GRI studies on Uber and Lyft algorithmic management, Keys AI Connect agentic delegation, the AI Compliance Paradox, and institutional governance. It extends the comparative research question: **Who retains responsibility when an algorithm recommends a decision, the human accepts it, and the system is later modified through feedback?**

### Evidence integrity and publication limits
As of this working protocol, the study is not a validated accuracy assessment or peer reviewed publication. Its small retrospective evidence inventory is vulnerable to selection bias, missing outcomes, and recall error. No claim of autonomous foundation model learning, reliable sports prediction, superior returns, or institutional endorsement is made. A prior four page GRI Sports Forecasting Research Framework PDF informed this protocol; the PDF binary is distributed separately and is not represented as included in this GitHub commit.

### Selected scholarly grounding
- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2
- Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of ICML*. https://proceedings.mlr.press/v70/guo17a.html
- Kellogg, K. C., Valentine, M. A., & Christin, A. (2020). Algorithms at work: The new contested terrain of control. *Academy of Management Annals*, 14(1), 366–410. https://doi.org/10.5465/annals.2018.0174
- Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. *Journal of Experimental Psychology: General*, 144(1), 114–126. https://doi.org/10.1037/xge0000033

*Independent Grand Research Institute working research. The study protocol and any eventual results must be versioned separately.*
