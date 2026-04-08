# ☁️ AWS Cloud Cost Estimator

A Python tool that estimates monthly AWS infrastructure costs for **EC2**, **S3**, and **RDS** resources — ideal for cloud budgeting and capacity planning.

## 🚀 Features

- ✅ EC2 instance cost calculator (supports t2, t3, m5, c5 families)
- ✅ S3 storage + data transfer cost estimator
- ✅ RDS database cost calculator (with Multi-AZ support)
- ✅ Interactive CLI mode — enter your own configuration
- ✅ Demo mode — pre-built production web app estimate
- ✅ Annual cost projection

## 🛠️ Tech Stack

- Python 3.x
- `dataclasses` (built-in)
- AWS on-demand pricing data (EC2, S3, RDS)

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/aws-cost-estimator.git
cd aws-cost-estimator
python cloud_cost_estimator.py
```

No external dependencies required!

## 📸 Demo Output

```
=======================================================
  AWS Cost Estimate — Web App — Production
=======================================================

  [ EC2 Instances ]
  EC2 t3.medium x2 (24.0h/day) = $74.88/mo
  EC2 t2.micro x1 (8.0h/day)   = $2.78/mo

  [ S3 Storage ]
  S3 Storage 100GB + 50GB transfer = $9.30/mo

  [ RDS Databases ]
  RDS db.t3.medium (Multi-AZ) + 50GB storage = $163.35/mo

───────────────────────────────────────────────────────
  TOTAL ESTIMATED COST : $250.31 / month
                       : $3,003.72 / year
=======================================================
```

## 🗺️ Roadmap

- [ ] Add Lambda & CloudFront pricing
- [ ] Export estimates to CSV/PDF
- [ ] Load configs from YAML file
- [ ] Compare Reserved vs On-Demand pricing

## 💡 What I Learned

- Learned how AWS pricing works for different services
- Understood concepts like compute, storage, and pricing models
- Improved logic building for cost calculation

## 🚧 Challenges Faced

- Understanding AWS pricing structure was confusing at first
- Handling different pricing units (hourly, monthly, storage size)
- Making the calculation logic accurate

## Future Improvements
  
- Add more AWS services
- Integrate real-time AWS pricing API
- Improve UI for better user experience
  
## 📄 License

MIT License

---
*Built while learning cybersecurity and cloud concepts*
