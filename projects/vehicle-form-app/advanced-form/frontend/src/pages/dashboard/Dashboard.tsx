import { useState } from "react"; // react hook to keep track of state
import Styles from "./Dashboard.module.css"; // css module for dashboard styles

// components that live inside the dashboard tabs
import Metrics from "../../components/dashboard/Metrics";
import VehicleForm from "../../components/dashboard/VehicleForm";
import About from "../../components/dashboard/About";

export default function Dashboard() {
    // keep track of which tab is active
    // the type <"metrics" | "form" | "about"> means it can only be these 3 values
    const [activeTab, setActiveTab] = useState<"metrics" | "form" | "about">(
        "metrics" // default tab when dashboard first loads
    );

    // define all tabs here
    // key = internal value, label = what user sees on button
    const tabs = [
        { key: "metrics", label: "Dashboard" },
        { key: "form", label: "Form" },
        { key: "about", label: "About Us" },
        // you had duplicate abouts before, remove if you don't want duplicates
    ];

    return (
        // container for whole dashboard, includes margin/padding + main container css
        <div className={`container-md mt-5 mb-3 px-4 ${Styles.mainContainer}`}>

            {/* button group for tabs */}
            <div className="btn-group mb-4">
                {tabs.map((tab) => (
                    // create one button per tab
                    <button
                        key={tab.key} // react needs unique keys for lists
                        className={`${Styles.tabButton} ${activeTab === tab.key ? Styles.tabButtonActive : ""}`} // highlight active tab
                        onClick={() =>
                            setActiveTab(tab.key as "metrics" | "form" | "about") // switch tab when clicked
                        }
                    >
                        {tab.label} {/* show user-friendly name */}
                    </button>
                ))}
            </div>

            {/* tab content area */}
            <div className={Styles.tabContent}>
                {/* show metrics tab only if active */}
                <div className={activeTab === "metrics" ? "" : Styles.hidden}>
                    <Metrics /> {/* this is the dashboard metrics component */}
                </div>

                {/* show form tab only if active */}
                <div className={activeTab === "form" ? "" : Styles.hidden}>
                    <VehicleForm /> {/* this is the vehicle form */}
                </div>

                {/* show about tab only if active */}
                <div className={activeTab === "about" ? "" : Styles.hidden}>
                    <About /> {/* about us info */}
                </div>
            </div>
        </div>
    );
}
