# Lab 01 - Azure cloud Manage Virtual Machines

## Lab introduction

In this lab, you create and compare virtual machines to virtual machine scale sets. You learn how to create, configure, and resize a single virtual machine. Finally, we will use Azure CLI to build a virtual machine.

This lab requires an Azure subscription. Your subscription type may affect the availability of features in this lab. You may change the region, but the steps are written using **East US**.

## Estimated timing: 50 minutes

## Lab scenario

Your organization wants to explore deploying and configuring Azure virtual machines. First, you implement an Azure virtual machine with manual scaling. Next, you explore the use of Azure Command Line to build your future infrastructure.


## Job skills

+ Task 1: Deploy zone-resilient Azure virtual machines by using the Azure portal.
+ Task 2: Manage compute and storage scaling for virtual machines.
+ Task 3: Create a virtual machine using the CLI
+ Task 4: Deploy an Apache web server
+ Task 5: Deploy a webapp 

## Azure Virtual Machines Architecture Diagram

![Diagram of the vm architecture tasks.](media/az104-lab08-vm-architecture.png)

## Instructions

### Before you start

#### Sign in to the lab environment

Sign in to your Windows 11 virtual machine (VM).

> **Note**: Your instructor will provide instructions to connect to the virtual lab environment.


## Task 1: Deploy zone-resilient Azure virtual machines by using the Azure portal

In this task, you will deploy two Azure virtual machines into different availability zones by using the Azure portal. Availability zones offer the highest level of uptime SLA for virtual machines at 99.99%. To achieve this SLA, you must deploy at least two virtual machines across different availability zones.

1. Sign in to the Azure portal - `https://portal.azure.com`.

1. Search for and select `Virtual machines`, on the **Virtual machines** blade, click **+ Create**, and then select in the drop-down **Azure virtual machine**. Notice your other choices.

1. On the **Basics** tab, in the **Availability zone** drop down menu, place a checkmark next to **Zone 2**. This should select both **Zone 1** and **Zone 2**.

    >**Note**: This will deploy two virtual machines in the selected region, one in each zone. You achieve the 99.99% uptime SLA because you have at least two VMs distributed across at least two zones. In the scenario where you might only need one VM, it is a best practice to still deploy the VM to another zone.

1. On the Basics tab, continue completing the configuration,:

    | Setting | Value |
    | --- | --- |
    | Subscription | the name of your Azure subscription |
    | Resource group |  select the resource group **Training-Student-0xx-Lab01** |
    | Virtual machine names | `lab01-vm1` and `lab01-vm2` (After selecting both availability zones, select **Edit names** under the VM name field.) |
    | Region | **East US** |
    | Availability options | **Availability zone** |
    | Availability zone | **Zone 1, 2** (read the note about using virtual machine scale sets) |
    | Security type | **Standard** |
    | Image | **Windows Server 2019 Datacenter - x64 Gen2** |
    | Azure Spot instance | **unchecked** |
    | Size | click on the link "See all sizes", then select **Standard B1s** |
    | Username | `localadmin` |
    | Password | **Provide a secure password** |
    | Public inbound ports | **None** |
    | Would you like to use an existing Windows Server license? | **Unchecked** |


1. Click **Next : Disks >** , specify the following settings (leave others with their default values):

    | Setting | Value |
    | --- | --- |
    | OS disk type | **HDD Standard** |
    | Delete with VM | **checked** (default) |
    | Enable Ultra Disk compatibility | **Unchecked** |

1. Click **Next : Networking >** take the defaults but do not provide a load balancer.

    | Setting | Value |
    | --- | --- |
    | Delete public IP and NIC when VM is deleted | **Checked** |
    | Load balancing options | **None** |


1. Click **Next : Management >** and specify the following settings (leave others with their default values):

    | Setting | Value |
    | --- | --- |
    | Patch orchestration options | **Azure orchestrated** |  

1. Click **Next : Monitoring >** and specify the following settings (leave others with their default values):

    | Setting | Value |
    | --- | --- |
    | Boot diagnostics | **Disable** |

1. Click **Next : Advanced >**, take the defaults, then click **Review + Create**.

1. After the validation, click **Create**.

    >**Note:** Notice as the virtual machine deploys the NIC, disk, and public IP address (if configured) are independently created and managed resources.

1. Wait for the deployment to complete, then select **Go to resource**.

   >**Note:** Monitor the **Notification** messages.

## Task 2: Manage compute and storage scaling for virtual machines

In this task, you will scale a virtual machine by adjusting its size to a different SKU. Azure provides flexibility in VM size selection so that you can adjust a VM for periods of time if it needs more (or less) compute and memory allocated. This concept is extended to disks, where you can modify the performance of the disk, or increase the allocated capacity.

1. On the **lab01-vm1** virtual machine, in the **Availability + scale** blade, select **Size**.

1. Set the virtual machine size to **B2s** and click **Resize**. When prompted, confirm the change.

    >**Note**: Choose another size if **B2s** is not available. Resizing is also known as vertical scaling, up or down.

    ![Screenshot of the resize the virtual machine.](media/az104-lab08-resize-vm.png)

1. In the **Settings** area, select **Disks**.

1. Under **Data disks** select **+ Create and attach a new disk**. Configure the settings (leave other settings at their default values).

    | Setting | Value |
    | --- | --- |
    | Disk name | `vm1-disk1` |
    | Storage type | **Standard HDD** |
    | Size (GiB) | `32` |

1. Click **Apply**.

1. After the disk has been created, click **Detach** (if necessary, scroll to the right to view the detach icon), and then click **Apply**.

    >**Note**: Detaching removes the disk from the VM but keeps it in storage for later use.

1. Search for and select `Disks`. From the list of disks, select the **vm1-disk1** object.

    >**Note:** The **Overview** blade also provides performance and usage information for the disk.

1. In the **Settings** blade, select **Size + performance**.

1. Set the storage type to **Standard SSD**, and then click **Save**.

1. Navigate back to the **lab01-vm1** virtual machine and select **Disks**.

1. In the **Data disk** section, select **Attach existing disks**.

1. In the **Disk name** drop-down, select **VM1-DISK1**. 

1. Verify the disk is now **Standard SSD**.

1. Select **Apply** to save your changes. 

    >**Note:** You have now created a virtual machine, scaled the SKU and the data disk size. In the next task we use Virtual Machine Scale Sets to automate the scaling process.


## Task 3: Create a virtual machine using the CLI 

1. Use the icon (top right) to launch a **Cloud Shell** session. Alternately, navigate directly to `https://shell.azure.com`.

1. Be sure to select **Bash**. Select the subscription Azure Subscription 1 ( the only one available ) and select apply.

1. Run the following command to create a virtual machine. When prompted, provide a username and password for the VM. While you wait check out the [az vm create](https://learn.microsoft.com/cli/azure/vm?view=azure-cli-latest#az-vm-create) command reference for all the parameters associated with creating a virtual machine.

    >**Note:** Replace **** with your own resource group.

    ```sh
    az vm create --name myCLIVM --resource-group  --image Ubuntu2204 --admin-username localadmin --generate-ssh-keys --size Standard_B1s
    ```

1. Once the command completes, use **az vm show** to verify your machine was created.

    >**Note:** Replace **** with your own resource group.
    
    ```sh
    az vm show --name  myCLIVM --resource-group  --show-details
    ```



## Task 4 : Setup our Apache webserver

1. Find the public IP of your VM, replacing with your assigned resource group.

```
az vm show --name myCLIVM --resource-group <> -d --query publicIps -o tsv
```

2. SSH into your VM.
   
```
ssh localadmin@<Public-IP>
```

3. First time SSH warning, type yes and press enter:
   
```
Are you sure you want to continue connecting (yes/no/[fingerprint])? 
```

4. Update your servers packages.
   
```
sudo apt update
```

5. Install Apache
   
```
sudo apt install apache2 -y
```

6. Start & Enable the service 

```
sudo systemctl start apache2
sudo systemctl enable apache2

```

### Allow Inbound Traffic through port 80 from any source

1. Navigate to your azure portal resource group

2. Look for **myCLIVMNSG** ( or the name of your VM from step 1 )

3. On the left panel, go to Settings > Inbound Security Rules

4. Hit the add

5. In the new pop up window, change Destination port ranges to **80**, and validate with Add  


Check if you can access your apache landing page

```
http://<Your-VM-Public-IP>/index.html
```

### Deallocate your VM


1. Use **az vm deallocate** to deallocate your virtual machine. Type **Yes** to confirm.

    >**Note:** Replace **** with your own resource group.
    
    ```sh
    az vm deallocate --resource-group  --name myCLIVM
    ```

2. Verify the **powerState** is **VM Running**.


3. Use **az vm show** to ensure the **powerState** is **VM deallocated**.

    >**Did you know?** When you use Azure to stop your virtual machine, the status is *deallocated*. This means that any non-static public IPs are released, and you stop paying for the VM’s compute costs.


## Cleanup your resources

1. When you are done with the lab, delete the resource group you created, we will use a different one for our future labs !
2. Go to Azure Portal, Navigate to your Resource Group
3. Hit the Delete Resource Group button with the bin. It will ask for your confirmation, type the resource group name and hit delete.


## Learn more with self-paced training

+ [Create a Windows virtual machine in Azure](https://learn.microsoft.com/training/modules/create-windows-virtual-machine-in-azure/). Create a Windows virtual machine using the Azure portal. Connect to a running Windows virtual machine using Remote Desktop
+ [Build a scalable application with Virtual Machine Scale Sets](https://learn.microsoft.com/training/modules/build-app-with-scale-sets/). Enable your application to automatically adjust to changes in load while minimizing costs with Virtual Machine Scale Sets.
+ [Connect to virtual machines through the Azure portal by using Azure Bastion](https://learn.microsoft.com/en-us/training/modules/connect-vm-with-azure-bastion/). Deploy Azure Bastion to securely connect to Azure virtual machines directly within the Azure portal to effectively replace an existing jumpbox solution, monitor remote sessions by using diagnostic logs, and manage remote sessions by disconnecting a user session.

## Key takeaways

Congratulations on completing the lab. Here are the main takeaways for this lab.

+ Azure virtual machines are on-demand, scalable computing resources.
+ Azure virtual machines provide both vertical and horizontal scaling options.
+ Configuring Azure virtual machines includes choosing an operating system, size, storage and networking settings.
+ Azure Virtual Machine Scale Sets let you create and manage a group of load balanced VMs.
+ The virtual machines in a Virtual Machine Scale Set are created from the same image and configuration.
+ In a Virtual Machine Scale Set the number of VM instances can automatically increase or decrease in response to demand or a defined schedule.
