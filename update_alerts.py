from pathlib import Path

path = Path("app/static/index.html")

text = path.read_text(encoding="utf-8")

start_marker = """            /* =========================
               FRAUD ALERTS
            ========================= */"""

end_marker = """            /* =========================
               CHART
            ========================= */"""

start = text.index(start_marker)
end = text.index(end_marker, start)

new_alerts = """            /* =========================
               FRAUD ALERTS
            ========================= */

            const alerts =
                document.getElementById("alerts");

            alerts.innerHTML = "";

            const highRiskTransactions =
                data.filter(
                    t => t.risk_level === "HIGH"
                );

            if (highRiskTransactions.length === 0) {

                alerts.innerHTML = `
                    <div class="no-alert">
                        &#9989; No high-risk transactions detected.
                    </div>
                `;

            }

            highRiskTransactions.forEach(
                transaction => {

                    const alert =
                        document.createElement("div");

                    alert.className = "alert";

                    const reasons =
                        Array.isArray(transaction.reasons)
                            ? transaction.reasons
                            : [];

                    const reasonHTML =
                        reasons
                            .filter(r => r.points > 0)
                            .map(
                                r =>
                                    `<li>${r.reason} (+${r.points})</li>`
                            )
                            .join("");

                    alert.innerHTML = `

                        <div class="alert-title">
                            &#128680; HIGH RISK TRANSACTION
                        </div>

                        <div class="alert-info">

                            Transaction:
                            <strong>
                                ${transaction.transaction_id}
                            </strong>

                            <br>

                            Amount:
                            &#8377;${Number(
                                transaction.amount
                            ).toLocaleString("en-IN")}

                            <br>

                            Risk Score:
                            <strong>
                                ${transaction.risk_score}
                            </strong>

                            <br>

                            Decision:
                            <strong>
                                ${transaction.decision}
                            </strong>

                            <br><br>

                            <strong>Risk factors:</strong>

                            <ul class="alert-reasons">
                                ${reasonHTML || "<li>Risk factors detected</li>"}
                            </ul>

                        </div>

                    `;

                    alerts.appendChild(alert);

                }
            );


"""

updated = text[:start] + new_alerts + text[end:]

path.write_text(updated, encoding="utf-8")

print("Alert section updated successfully.")