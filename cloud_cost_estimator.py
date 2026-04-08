"""
AWS Cloud Cost Estimator
Cloud Computing Project | Python
Estimates monthly AWS costs for EC2, S3, and RDS resources.
"""

from dataclasses import dataclass, field
from typing import List


# --- Pricing Data (USD, approximate on-demand prices) ---

EC2_PRICING = {
    "t2.micro":    0.0116,
    "t2.small":    0.023,
    "t2.medium":   0.0464,
    "t3.medium":   0.0416,
    "m5.large":    0.096,
    "m5.xlarge":   0.192,
    "c5.large":    0.085,
    "c5.xlarge":   0.17,
}

S3_PRICING = {
    "storage_per_gb":        0.023,    # First 50 TB / month
    "put_per_1000":          0.005,    # PUT requests
    "get_per_1000":          0.0004,   # GET requests
    "data_transfer_per_gb":  0.09,     # Out to internet
}

RDS_PRICING = {
    "db.t3.micro":   0.017,
    "db.t3.small":   0.034,
    "db.t3.medium":  0.068,
    "db.m5.large":   0.171,
    "storage_per_gb_month": 0.115,
}


@dataclass
class EC2Instance:
    instance_type: str
    count: int = 1
    hours_per_day: float = 24.0
    days_per_month: int = 30

    def monthly_cost(self) -> float:
        hourly = EC2_PRICING.get(self.instance_type, 0)
        return hourly * self.hours_per_day * self.days_per_month * self.count

    def summary(self) -> str:
        return (f"  EC2 {self.instance_type} x{self.count} "
                f"({self.hours_per_day}h/day) = ${self.monthly_cost():.2f}/mo")


@dataclass
class S3Bucket:
    storage_gb: float = 0.0
    put_requests_k: float = 0.0   # In thousands
    get_requests_k: float = 0.0
    data_transfer_gb: float = 0.0

    def monthly_cost(self) -> float:
        return (
            self.storage_gb        * S3_PRICING["storage_per_gb"] +
            self.put_requests_k    * S3_PRICING["put_per_1000"] +
            self.get_requests_k    * S3_PRICING["get_per_1000"] +
            self.data_transfer_gb  * S3_PRICING["data_transfer_per_gb"]
        )

    def summary(self) -> str:
        return (f"  S3 Storage {self.storage_gb}GB + "
                f"{self.data_transfer_gb}GB transfer = ${self.monthly_cost():.2f}/mo")


@dataclass
class RDSInstance:
    instance_type: str
    storage_gb: float = 20.0
    hours_per_day: float = 24.0
    days_per_month: int = 30
    multi_az: bool = False

    def monthly_cost(self) -> float:
        hourly = RDS_PRICING.get(self.instance_type, 0)
        if self.multi_az:
            hourly *= 2
        compute = hourly * self.hours_per_day * self.days_per_month
        storage = self.storage_gb * RDS_PRICING["storage_per_gb_month"]
        return compute + storage

    def summary(self) -> str:
        az = " (Multi-AZ)" if self.multi_az else ""
        return (f"  RDS {self.instance_type}{az} + "
                f"{self.storage_gb}GB storage = ${self.monthly_cost():.2f}/mo")


@dataclass
class CloudInfrastructure:
    name: str
    ec2_instances: List[EC2Instance] = field(default_factory=list)
    s3_buckets:    List[S3Bucket]    = field(default_factory=list)
    rds_instances: List[RDSInstance] = field(default_factory=list)

    def total_cost(self) -> float:
        return (
            sum(i.monthly_cost() for i in self.ec2_instances) +
            sum(b.monthly_cost() for b in self.s3_buckets) +
            sum(r.monthly_cost() for r in self.rds_instances)
        )

    def print_report(self):
        print(f"\n{'='*55}")
        print(f"  AWS Cost Estimate — {self.name}")
        print(f"{'='*55}")

        if self.ec2_instances:
            print("\n  [ EC2 Instances ]")
            for i in self.ec2_instances:
                print(i.summary())

        if self.s3_buckets:
            print("\n  [ S3 Storage ]")
            for b in self.s3_buckets:
                print(b.summary())

        if self.rds_instances:
            print("\n  [ RDS Databases ]")
            for r in self.rds_instances:
                print(r.summary())

        total = self.total_cost()
        print(f"\n{'─'*55}")
        print(f"  TOTAL ESTIMATED COST : ${total:.2f} / month")
        print(f"                       : ${total * 12:.2f} / year")
        print(f"{'='*55}\n")


def interactive_estimator():
    print("\n=== AWS Cloud Cost Estimator ===")
    print("   Cloud Computing Tool | Python\n")

    name = input("Project/Environment name (e.g. 'Production'): ").strip() or "My Project"
    infra = CloudInfrastructure(name=name)

    # EC2
    print("\n--- EC2 Instances ---")
    print("Available types:", ", ".join(EC2_PRICING.keys()))
    while True:
        itype = input("EC2 instance type (or Enter to skip): ").strip()
        if not itype:
            break
        if itype not in EC2_PRICING:
            print("  Unknown type. Try again.")
            continue
        count = int(input("  How many? ") or 1)
        hours = float(input("  Hours per day running? (default 24): ") or 24)
        infra.ec2_instances.append(EC2Instance(itype, count, hours))

    # S3
    print("\n--- S3 Storage ---")
    add_s3 = input("Add S3 bucket? (y/n): ").strip().lower()
    if add_s3 == "y":
        gb = float(input("  Storage GB: ") or 0)
        transfer = float(input("  Data transfer out GB: ") or 0)
        infra.s3_buckets.append(S3Bucket(storage_gb=gb, data_transfer_gb=transfer))

    # RDS
    print("\n--- RDS Database ---")
    print("Available types:", ", ".join(k for k in RDS_PRICING if k != "storage_per_gb_month"))
    add_rds = input("Add RDS instance? (y/n): ").strip().lower()
    if add_rds == "y":
        rtype = input("  RDS instance type: ").strip()
        storage = float(input("  Storage GB (default 20): ") or 20)
        multi_az = input("  Multi-AZ? (y/n): ").strip().lower() == "y"
        infra.rds_instances.append(RDSInstance(rtype, storage, multi_az=multi_az))

    infra.print_report()


def demo():
    """Run a pre-built demo estimate for a typical web app."""
    infra = CloudInfrastructure(
        name="Web App — Production",
        ec2_instances=[
            EC2Instance("t3.medium", count=2, hours_per_day=24),
            EC2Instance("t2.micro",  count=1, hours_per_day=8),
        ],
        s3_buckets=[
            S3Bucket(storage_gb=100, put_requests_k=500, get_requests_k=2000, data_transfer_gb=50),
        ],
        rds_instances=[
            RDSInstance("db.t3.medium", storage_gb=50, multi_az=True),
        ]
    )
    infra.print_report()


if __name__ == "__main__":
    print("\n1. Interactive estimator")
    print("2. Run demo (pre-built web app estimate)")
    choice = input("Choose (1/2): ").strip()
    if choice == "2":
        demo()
    else:
        interactive_estimator()
