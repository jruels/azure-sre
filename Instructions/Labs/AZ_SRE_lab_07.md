# Lab 07 - Manage Virtual Machines Scale Sets

## Lab introduction

In this lab, you learn how to create a virtual machine scale set and configure autoscaling.

This lab requires an Azure subscription. Your subscription type may affect the availability of features in this lab. You may change the region, but the steps are written using **East US**.

## Estimated timing: 50 minutes

## Lab scenario

Your organization wants to explore automatic scaling. You implement a Virtual Machine Scale Set and explore autoscaling.

## Job skills

+ Task 1: Create and configure Azure Virtual Machine Scale Sets.
+ Task 2: Scale Azure Virtual Machine Scale Sets.
+ Task 3: Monitor at Scale


## Instructions

### Before you start

#### Sign in to the lab environment

Sign in to your Windows 11 virtual machine (VM).

> **Note**: Your instructor will provide instructions to connect to the virtual lab environment.


## Azure Virtual Machine Scale Sets Architecture Diagram

![Diagram of the vmss architecture tasks.](media/az104-lab08-vmss-architecture.png)

## Task 1: Create and configure Azure Virtual Machine Scale Sets

In this task, you will deploy an Azure virtual machine scale set across availability zones. VM Scale Sets reduce the administrative overhead of automation by enabling you to configure metrics or conditions that allow the scale set to horizontally scale, scale in or scale out.

1. In the Azure portal, search for and select `Virtual machine scale sets` and, on the **Virtual machine scale sets** blade, click **+ Create**.

1. On the **Basics** tab of the **Create a virtual machine scale set** blade, specify the following settings (leave others with their default values) and click **Next : Spot >**:

    | Setting | Value |
    | --- | --- |
    | Subscription | the name of your Azure subscription  |
    | Resource group | **Training-Student-0xx-OC0xx** |
    | Virtual machine scale set name | `vmss1` |
    | Region | **(US)East US** |
    | Availability zone | **Zones 1, 2, 3** |
    | Orchestration mode | **Uniform** |
    | Security type | **Standard** |
    | Scaling options | **Review and take the defaults**. We will change this in the next task. |
    | Image | **Windows Server 2019 Datacenter - x64 Gen2** |
    | Run with Azure Spot discount | **Unchecked** |
    | Size | click on the link "See all sizes", then select **Standard B1s** |
    | Username | `localadmin` |
    | Password | **Provide a secure password**  |
    | Already have a Windows Server license? | **Unchecked** |

    > **Notes:** For the list of Azure regions which support deployment of Windows virtual machines to availability zones, refer to [What are Availability Zones in Azure?](https://docs.microsoft.com/en-us/azure/availability-zones/az-overview)

    ![Screenshot of the create vmss page. ](media/az104-lab08-create-vmss.png)

1. On the **Spot** tab, accept the defaults and select **Next : Disks >**.

1. On the **Disks** tab, accept the default values and click **Next : Networking >**.

1. On the **Networking** page, select **Edit virtual network** link. Make a few changes. When finished, select **OK**.

    | Setting | Value |
    | --- | --- |
    | Name | `vmss-vnet` |
    | Address range | `10.82.0.0/20` (delete the existing address range) |
    | Subnet name | `subnet0` |
    | Subnet range | `10.82.0.0/24` |

1. In the **Networking** tab, click the **Edit network interface** icon to the right of the network interface entry.

1. For **NIC network security group** section, select **Advanced** and then click **Create new** under the **Configure network security group** drop-down list.

1. On the **Create network security group** blade, specify the following settings (leave others with their default values):

    | Setting | Value |
    | --- | --- |
    | Name | **vmss1-nsg** |

1. Click **Add an inbound rule** and add an inbound security rule with the following settings (leave others with their default values):

    | Setting | Value |
    | --- | --- |
    | Source | **Any** |
    | Source port ranges | * |
    | Destination | **Any** |
    | Service | **HTTP** |
    | Action | **Allow** |
    | Priority | **1010** |
    | Name | `allow-http` |

1. Click **Add** and, back on the **Create network security group** blade, click **OK**.

1. In the **Edit network interface** blade, in the **Public IP address** section, click **Enabled** and click **OK**.

1. In the **Networking** tab, under the **Load balancing** section, specify the following (leave others with their default values).

    | Setting | Value |
    | --- | --- |
    | Load balancing options | **Azure load balancer** |
    | Select a load balancer | **Create a load balancer** |

1. On the **Create a load balancer** page, specify the load balancer name and take the defaults. Click **Create** when you are done then **Next : Management >**.

    | Setting | Value |
    | --- | --- |
    | Load balancer name | `vmss-lb` |

    > **Notes:** Pause for a minute and review what you done. At this point, you have configured the virtual machine scale set with disks and networking. In the network configuration you have created a network security group and allowed HTTP. You have also created a load balancer with a public IP address.

1. On the **Management** tab, specify the following settings (leave others with their default values):

    | Setting | Value |
    | --- | --- |
    | Boot diagnostics | **Disable** |

1. Click **Next : Health >**.

1. On the **Health** tab, review the default settings without making any changes and click **Next : Advanced >**.

1. On the **Advanced** tab, click **Review + create**.

1. On the **Review + create** tab, ensure that the validation passed and click **Create**.

    > **Notes:** Wait for the virtual machine scale set deployment to complete. This should take approximately 5 minutes. While you wait review the [documentation](https://learn.microsoft.com/azure/virtual-machine-scale-sets/overview).

---

## Task 2: Scale Azure Virtual Machine Scale Sets

In this task, you scale the virtual machine scale set using a custom scale rule.

1. Select **Go to resource** or search for and select the **vmss1** scale set.

1. Choose **Availability + Scale** from the left side menu, then choose **Scaling**.

    > **Did you know?** You can **Manual scale** or **Custom autoscale**. In scale sets with a small number of VM instances, increasing or decreasing the instance count (Manual scale) may be best. In scale sets with a large number of VM instances, scaling based on metrics (Custom autoscale) may be more appropriate.

**Scale out rule**

1. Select **Custom autoscale**. Then change the **Scale mode** to **Scale based on metric**. And then select **Add a rule**.

1. Let's create a rule that automatically increases the number of VM instances. This rule scales out when the average CPU load is greater than 70% over a 10-minute period. When the rule triggers, the number of VM instances is increased by 50%.

    | Setting | Value |
    | --- | --- |
    | Metric source | **Current resource (vmss1)** |
    | Metric namespace | **Virtual Machine Host** |
    | Metric name | **Percentage CPU** (review your other choices) |
    | Operator | **Greater than** |
    | Metric threshold to trigger scale action | **70** |
    | Duration (minutes) | **10** |
    | Time grain statistic | **Average** |
    | Operation | **Increase percent by** (review other choices) |
    | Cool down (minutes) | **5** |
    | Percentage | **50** |

    ![Screenshot of the scaling add rule page.](media/az104-lab08-scale-rule.png)

1. Be sure to **Save** your changes.

**Scale in rule**

1. During evenings or weekends, demand may decrease so it is important to create a scale in rule.

1. Let's create a rule that decreases the number of VM instances in a scale set. The number of instances should decrease when the average CPU load drops below 30% over a 10-minute period. When the rule triggers, the number of VM instances is decreased by 20%.

1. Select **Add a rule**, adjust the settings, then select **Add**.

    | Setting | Value |
    | --- | --- |
    | Operator | **Less than** |
    | Threshold | **30** |
    | Operation | **decrease percentage by** (review your other choices) |
    | Percentage | **50** |

1. Be sure to **Save** your changes.

**Set the instance limits**

1. When your autoscale rules are applied, instance limits make sure that you do not scale out beyond the maximum number of instances or scale in beyond the minimum number of instances.

1. **Instance limits** are shown on the **Scaling** page after the rules.

    | Setting | Value |
    | --- | --- |
    | Minimum | **2** |
    | Maximum | **10** |
    | Default | **2** |

1. Be sure to **Save** your changes

1. On the **vmss1** page, select **Instances**. This is where you would monitor the number of virtual machine instances.

    > **Notes:**  If you are interested in using Azure PowerShell for virtual machine creation, try Task 5. If you are interested in using the CLI to create virtual machines, try Task 6.

---

## Task 3: Create and configure Azure Virtual Machine Scale Sets


### Step 1: Login to your machine

1. Go to the Azure portal.
2. Navigate to **Virtual machine scale sets > vmss1 > Instances**.
3. Select an instance (e.g., `vmss1_0`).
4. Click **Connect > Bastion**.
5. Log in using:
   - **Username**: `localadmin`
   - **Password**: (the one you set during VMSS creation)



### Step 2: Open PowerShell and Run CPU Stress Script
1. Open **PowerShell as Administrator** inside the VM.
2. Run the following to simulate 100% CPU usage:

   ```powershell
   for ($i=0; $i -lt 10; $i++) {
     Start-Job -ScriptBlock { while ($true) {} }
   }
   ```

    > **Notes:**  This script launches 10 infinite loops in the background to max out CPU usage.

### Step 3: Wait and Observe Autoscaling
- Wait **10–15 minutes** to allow the autoscale rule to trigger.
- Navigate to:
  - **VMSS > Scaling > Run history** – to view autoscale event logs.
  - **VMSS > Instances** – to watch for new VM instances being added.

    > **Notes:** The scale out rule should trigger when CPU > 70% for 10 minutes.

---

## Task 4: Trigger VMSS to Scale In

### Step 1: Stop the CPU Load
1. In the same PowerShell session, run:

   ```powershell
   Get-Job | Stop-Job
   ```
This will terminate the infinite loops and reduce CPU usage.


### Step 2: Wait and Observe Scaling In
1. Wait **10–15 minutes** for the average CPU to drop below 30%.
1. Monitor:
   - **VMSS > Scaling > Run history**
   - **VMSS > Instances** – to observe VM instances being removed.

    > **Notes:** VMSS will scale back in according to the configured scale-in rule.

---

## Task 5: Visualize CPU Metrics in Azure Monitor

### Step 1: View Real-Time Metrics
1. Go to **Monitor > Metrics** in the Azure portal.
2. Set **Scope** to your `vmss1` resource.
3. Select:
   - **Metric Namespace**: `Virtual Machine Host`
   - **Metric**: `Percentage CPU`
4. Set **Aggregation** to `Average`.
5. Filter by instance, and optionally change granularity to **1 minute**.

---

## Key takeaways

Congratulations on completing the lab. Here are the main takeaways for this lab.

+ Azure Virtual Machine Scale Sets (VMSS) let you deploy and manage a group of identically-configured VMs that can automatically scale to match demand.  
+ Deploying a VMSS across multiple availability zones increases fault tolerance and availability.  
+ Networking and security must be defined during deployment. Including virtual network, subnet, network security group, public load balancer and public IP address.  
+ Custom autoscale rules enable precise control over when the scale set scales out or in, based on metrics such as average CPU utilization.  
+ Instance limits (minimum, maximum and default counts) protect against over- or under-provisioning when autoscale rules run.  
+ Azure Monitor provides real-time metrics and run-history logs so you can verify and troubleshoot autoscale events.  
+ Generating workload (for example, stressing CPU inside a VM) is an effective way to test that your scale-out and scale-in rules behave as expected.  
+ VMSS reduces operational overhead by automatically distributing traffic through the load balancer and maintaining consistent configuration across all instances.
