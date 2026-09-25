# Primary sources and evidence boundaries

This is an annotated reading list, not a substitute for per-system measurements, current implementation documentation, or a correctness proof. Read the source relevant to the chosen pattern and distinguish its assumptions from those of the target system.

## Foundations: coordination, consistency, and replication

1. **Ongaro and Ousterhout, "In Search of an Understandable Consensus Algorithm" (Raft, 2014).** Leader election, replicated log, safety, and membership change. Useful for deciding when critical shared state needs a consensus-backed replicated state machine. https://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14.pdf
2. **Google SRE, "Managing Critical State: Distributed Consensus for Reliability".** Operational costs and uses of consensus for critical state, leases, membership, and consistency. https://sre.google/sre-book/managing-critical-state/
3. **Shapiro, Preguiça, Baquero, and Zawirski, "A comprehensive study of Convergent and Commutative Replicated Data Types" (INRIA RR-7506, 2011).** Formal conditions for state- and operation-based CRDT convergence. https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf
4. **Das, Gupta, and Motivala, "SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol" (2002).** Separates membership dissemination from failure detection; membership suspicion is not agreement or guaranteed delivery. https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf
5. **Martin Kleppmann, "How to do distributed locking" (2016).** Why leases need fencing tokens enforced by the protected storage/resource. https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
6. **Martin Kleppmann, "Please stop calling databases CP or AP" (2015).** Clarifies the scope and common misuses of CAP labels. https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html

## Reliability, messaging, and recoverability

7. **Google SRE, "Addressing Cascading Failures" and "Handling Overload".** Load shedding, graceful degradation, retry budgets, and amplification across multiple layers. https://sre.google/sre-book/addressing-cascading-failures/ and https://sre.google/sre-book/handling-overload/
8. **Amazon Builders' Library, "Timeouts, retries, and backoff with jitter" (Marc Brooker, 2019).** Set timeouts intentionally; cap attempts and stagger retries without making overload worse. https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf
9. **Microsoft Azure Architecture Center, cloud design patterns.** Use the specific, current pattern document for idempotent consumers, bulkheads, circuit breakers, retry, queue-based load leveling, and compensating transactions rather than treating patterns as blanket prescriptions. https://learn.microsoft.com/en-us/azure/architecture/patterns/
10. **Apache Flink, "Fault Tolerance".** Exactly-once state effects require the right recovery protocol; end-to-end effect guarantees depend on replayable sources and idempotent or transactional sinks. https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/

## Testing and instrumentation

11. **Jepsen, "Analyses" and testing approach.** Real binaries with fault injection, generated concurrent histories, and property checkers can *find* correctness violations; passing tests is not a formal proof. https://jepsen.io/analyses and https://jepsen.io/services/analysis
12. **OpenTelemetry, "Context propagation".** Propagates distributed trace context; incoming trace context needs trust-boundary validation and baggage must not carry secrets. https://opentelemetry.io/docs/concepts/context-propagation/
13. **OpenTelemetry, messaging semantic conventions.** Correlates producer and consumer spans; check current spec stability/version before copying attribute names. https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/

## Source-to-decision discipline

- For an architectural recommendation, attach the **specific invariant and failure assumption** to the source. A documented pattern does not prove that a particular implementation satisfies it.
- For product-specific broker, cloud, driver, or database guarantees, verify the exact version and configuration in current official documentation and test the actual failure boundary.
- Preserve source URLs, dates/versions, caveats, dissenting evidence, and measured outcomes in the ADR or design packet.
- Do not make numerical capacity, consistency-latency, reliability, or convergence claims solely from general reading.
